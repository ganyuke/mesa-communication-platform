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

    from .views import views
    app.register_blueprint(views,url_prefix='/')

    db.init_app(app)
    if not path.exists("app/" + DB_NAME):
        db.create_all(app=app)

    from .models import User
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return(app)