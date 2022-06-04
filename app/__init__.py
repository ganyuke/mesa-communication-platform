from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import path, environ

db = SQLAlchemy()
DB_NAME = "database.sqlite3"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = environ.get("SECRET_KEY", "dev")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return(app)