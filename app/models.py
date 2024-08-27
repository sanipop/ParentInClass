# app/models.py
from flask_login import UserMixin
from datetime import datetime
from app import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(10))  # "admin" or "parent"
    # Define the relationship
    children = db.relationship('ChildRecord', backref='parent', lazy=True)
    

    def __repr__(self):
        return f'<User {self.username}>'

class ChildRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    child_name = db.Column(db.String(64), index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    attendance = db.Column(db.String(10))  # Example: "Present" or "Absent"
    classwork_score = db.Column(db.Float)
    homework_score = db.Column(db.Float)
    test_score = db.Column(db.Float)
    exam_score = db.Column(db.Float)
    notes = db.Column(db.Text)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ChildRecord {self.child_name}>'
