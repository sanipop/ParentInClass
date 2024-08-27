# app/__init__.py
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Define load_user with deferred import to avoid circular import
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User  # Deferred import to avoid circular import
        return User.query.get(int(user_id))    
    
    # Set the login view
    login_manager.login_view = 'main.login'
    

    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
