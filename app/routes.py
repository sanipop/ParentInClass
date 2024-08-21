from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user, UserMixin
from app import db, login_manager
from app.forms import LoginForm, RegistrationForm
from app.models import User
from app.routes import main


main = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        # Logic to validate user credentials
        return redirect(url_for('main.index'))
    return render_template('login.html', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Logic to register a new user
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)


@main.route('/parent_dashboard')
@login_required
def parent_dashboard():
    # Check if the user is a parent (you might have a role field in your User model)
    if current_user.role != 'parent':
        flash('Access Denied: You are not authorized to view this page.', 'danger')
        return redirect(url_for('main.index'))
    
    # Retrieve the child information related to the parent
    # Example: children = current_user.children (assuming a relationship is defined)
    children = []  # Placeholder for children data
    
    return render_template('parent_dashboard.html', children=children)

@main.route('/admin_dashboard')
@login_required
def admin_dashboard():
    # Check if the user is an administrator
    if current_user.role != 'admin':
        flash('Access Denied: You are not authorized to view this page.', 'danger')
        return redirect(url_for('main.index'))
    
    # Admin dashboard might display a list of students, their records, etc.
    students = []  # Placeholder for student data
    
    return render_template('admin_dashboard.html', students=students)
