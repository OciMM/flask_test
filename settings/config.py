import os

class Config:
    SECRET_KEY = "supersecretkey"
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = "filesystem"

    SECRET_KEY = os.environ.get("SECRET_KEY") or "supersecretkey"
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = SECRET_KEY  # Секретный ключ для CSRF