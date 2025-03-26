from flask import Flask
from settings.config import Config
from settings.models import db, bcrypt
from settings.routes import api
from flask_session import Session
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
app.config.from_object(Config)


csrf = CSRFProtect(app) 


db.init_app(app)
bcrypt.init_app(app)
Session(app)


app.register_blueprint(api)


with app.app_context():
    db.create_all()    # Создать таблицы, если их нет


if __name__ == "__main__":
    app.run(debug=True)