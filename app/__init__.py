# app/__init__.py
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
