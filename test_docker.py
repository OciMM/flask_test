import requests

# Регистрация пользователя

base_url = "http://localhost:5000"

# Получаем CSRF-токен
session = requests.Session()
csrf_response = session.get(f"{base_url}/api/csrf-token")
csrf_token = csrf_response.json().get("csrf_token")

# Регистрируем пользователя с CSRF-токеном
response = session.post(f"{base_url}/api/register_user", json={
    "login": "testuserw",
    "password": "password123w",
    "full_name": "Test User",
    "gender": "male",
    "birth_date": "1990-01-01"
}, headers={"X-CSRF-Token": csrf_token})

print(response.status_code, response.json())


# Выполняем вход с CSRF-токеном
response = session.post(f"{base_url}/api/login_user", json={
    "login": "testuser",
    "password": "password123"
}, headers={"X-CSRF-Token": csrf_token})

print(response.status_code, response.json())


# # Получение списка пользователей
response = requests.get(f"{base_url}/api/get_users")
print(response.status_code, response.json())