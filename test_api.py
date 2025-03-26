import pytest
from app import app, db
from settings.models import User

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # Используем in-memory SQLite
    app.config["SECRET_KEY"] = "test_secret_key"

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def get_csrf_token(client):
    """Функция для получения CSRF-токена."""
    response = client.get("/api/csrf-token")
    return response.json["csrf_token"]

def test_register_user(client):
    csrf_token = get_csrf_token(client)
    response = client.post("/api/register_user", json={
        "login": "testuser",
        "password": "password123",
        "full_name": "Test User",
        "gender": "male",
        "birth_date": "1990-01-01"
    }, headers={"X-CSRF-Token": csrf_token})
    
    assert response.status_code == 201
    assert response.json["message"] == "Пользователь зарегистрирован"

def test_register_duplicate_user(client):
    csrf_token = get_csrf_token(client)
    
    client.post("/api/register_user", json={
        "login": "testuser",
        "password": "password123",
        "full_name": "Test User",
        "gender": "male",
        "birth_date": "1990-01-01"
    }, headers={"X-CSRF-Token": csrf_token})
    
    csrf_token = get_csrf_token(client)  # Получаем новый CSRF-токен перед следующим запросом
    response = client.post("/api/register_user", json={
        "login": "testuser",
        "password": "password123",
        "full_name": "Another User",
        "gender": "female",
        "birth_date": "2000-01-01"
    }, headers={"X-CSRF-Token": csrf_token})
    
    assert response.status_code == 400
    assert response.json["error"] == "Пользователь уже существует"

def test_login_user(client):
    csrf_token = get_csrf_token(client)
    
    client.post("/api/register_user", json={
        "login": "testuser",
        "password": "password123",
        "full_name": "Test User",
        "gender": "male",
        "birth_date": "1990-01-01"
    }, headers={"X-CSRF-Token": csrf_token})
    
    csrf_token = get_csrf_token(client)
    response = client.post("/api/login_user", json={
        "login": "testuser",
        "password": "password123"
    }, headers={"X-CSRF-Token": csrf_token})
    
    assert response.status_code == 200
    assert response.json["message"] == "Вход выполнен"

def test_login_invalid_user(client):
    csrf_token = get_csrf_token(client)
    response = client.post("/api/login_user", json={
        "login": "wronguser",
        "password": "password123"
    }, headers={"X-CSRF-Token": csrf_token})
    
    assert response.status_code == 401
    assert response.json["error"] == "Неверный логин или пароль"

def test_get_users_not_logged_in(client):
    csrf_token = get_csrf_token(client)
    
    client.post("/api/register_user", json={
        "login": "testuser",
        "password": "password123",
        "full_name": "Test User",
        "gender": "male",
        "birth_date": "1990-01-01"
    }, headers={"X-CSRF-Token": csrf_token})
    
    response = client.get("/api/get_users")
    assert response.status_code == 200
    assert response.json == [{"login": "testuser"}]  # Должны увидеть только логины

def test_get_users_logged_in(client):
    csrf_token = get_csrf_token(client)
    
    client.post("/api/register_user", json={
        "login": "testuser",
        "password": "password123",
        "full_name": "Test User",
        "gender": "male",
        "birth_date": "1990-01-01"
    }, headers={"X-CSRF-Token": csrf_token})
    
    csrf_token = get_csrf_token(client)
    client.post("/api/login_user", json={
        "login": "testuser",
        "password": "password123"
    }, headers={"X-CSRF-Token": csrf_token})
    
    response = client.get("/api/get_users")
    assert response.status_code == 200
    assert response.json == [{
        "login": "testuser",
        "full_name": "Test User",
        "gender": "male",
        "birth_date": "1990-01-01"
    }]  # Должны увидеть все данные, так как залогинены
