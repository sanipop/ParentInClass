# app/routes.py
from flask import render_template, redirect, url_for, flash, current_app, Blueprint, request
from app import db
from app.models import User, ChildRecord
from app.forms import RegistrationForm, LoginForm, AddStudentForm, MarkAttendanceForm, AddTestForm, AddExamForm, AddClassworkForm, AddHomeworkForm
from app.models import User
from app.register_forms import ParentRegistrationForm, AdminRegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
 

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html')

@main.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('main.index'))
    return render_template('admin_dashboard.html')
