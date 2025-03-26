import re
from flask import Blueprint, request, jsonify, session
from settings.models import db, User
from flask_wtf.csrf import generate_csrf, validate_csrf

api = Blueprint("api", __name__)

# Валидация логина и пароля
def validate_login(login):
    return bool(re.match(r"^[a-zA-Z0-9]+$", login))

def validate_password(password):
    return len(password) >= 8

# Маршрут для получения CSRF-токена
@api.route("/api/csrf-token", methods=["GET"])
def get_csrf_token():
    csrf_token = generate_csrf()
    return jsonify({"csrf_token": csrf_token})

# Регистрация пользователя (с CSRF-защитой)
@api.route("/api/register_user", methods=["POST"])
def register_user():
    try:
        csrf_token = request.headers.get("X-CSRF-Token")
        validate_csrf(csrf_token)  # Проверяем CSRF-токен
    except Exception:
        return jsonify({"error": "Invalid CSRF token"}), 400

    data = request.json
    login = data.get("login")
    password = data.get("password")
    full_name = data.get("full_name")
    gender = data.get("gender")
    birth_date = data.get("birth_date")

    if not validate_login(login):
        return jsonify({"error": "Логин должен содержать только буквы и цифры"}), 400
    if not validate_password(password):
        return jsonify({"error": "Пароль должен содержать минимум 8 символов"}), 400
    if User.query.filter_by(login=login).first():
        return jsonify({"error": "Пользователь уже существует"}), 400

    user = User(login=login, full_name=full_name, gender=gender, birth_date=birth_date)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Пользователь зарегистрирован"}), 201

# Логин пользователя (с CSRF-защитой)
@api.route("/api/login_user", methods=["POST"])
def login_user():
    try:
        csrf_token = request.headers.get("X-CSRF-Token")
        validate_csrf(csrf_token)
    except Exception:
        return jsonify({"error": "Invalid CSRF token"}), 400

    data = request.json
    login = data.get("login")
    password = data.get("password")

    user = User.query.filter_by(login=login).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Неверный логин или пароль"}), 401

    session["user_id"] = user.id
    return jsonify({"message": "Вход выполнен"}), 200

# Получение пользователей (без CSRF-защиты, так как это GET-запрос)
@api.route("/api/get_users", methods=["GET"])
def get_users():
    if "user_id" in session:
        users = User.query.all()
        return jsonify([
            {"login": u.login, "full_name": u.full_name, "gender": u.gender, "birth_date": u.birth_date}
            for u in users
        ])

    users = User.query.with_entities(User.login).all()
    return jsonify([{"login": u.login} for u in users])
