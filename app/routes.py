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

@main.route('/parent_dashboard')
@login_required
def parent_dashboard():
    if current_user.role != 'parent':
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('main.index'))
    return render_template('parent_dashboard.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            if user.role == 'admin':
                return redirect(url_for('main.admin_dashboard'))
            elif user.role == 'parent':
                return redirect(url_for('main.parent_dashboard'))
        else:
            flash('Login unsuccessful. Please check your username and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@main.route('/register_parent', methods=['GET', 'POST'])
def register_parent():
    form = ParentRegistrationForm()
    
    # Populate the child_name choices dynamically from ChildRecord
    form.child_name.choices = [(child.id, child.child_name) for child in ChildRecord.query.all()]
    
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email address already in use. Please choose a different one.', 'danger')
            return redirect(url_for('main.register_parent'))        

        # Create a new Parent instance
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        parent = User(username=form.name.data, email=form.email.data, password_hash=hashed_password, role='parent')
        
        # Associate the selected child with the parent
        selected_child = ChildRecord.query.get(form.child_name.data)
        selected_child.parent_id = parent.id  # Set the parent_id in ChildRecord
        
        # Add and commit to the database
        db.session.add(parent)
        db.session.add(selected_child)  # Ensure the child's parent_id is committed
        db.session.commit()
        
        flash('Parent account created successfully!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('register_parent.html', title='Register as Parent', form=form)


@main.route('/register_admin', methods=['GET', 'POST'])
def register_admin():
    form = AdminRegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email address already in use. Please choose a different one.', 'danger')
            return redirect(url_for('main.register_admin'))        
        # Add the admin registration logic here
        # Create a new Admin instance
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        admin = User(username=form.name.data, email=form.email.data, password_hash=hashed_password, role='admin')
        # Add and commit to the database
        db.session.add(admin)
        db.session.commit()
        flash('Administrator account created successfully!', 'success')
        return redirect(url_for('main.index'))
    return render_template('register_admin.html', title='Register as Administrator', form=form)



#The Admin DashBoard functions
@main.route('/add_student', methods=['GET', 'POST'])
def add_student():
    form = AddStudentForm()
    if form.validate_on_submit():
        student = ChildRecord(child_name=form.child_name.data)
        db.session.add(student)
        db.session.commit()
        flash('Student added successfully!', 'success')
        return redirect(url_for('main.admin_dashboard'))
    return render_template('add_student.html', title='Add Student', form=form)

@main.route('/mark_attendance', methods=['GET', 'POST'])
def mark_attendance():
    form = MarkAttendanceForm()
    form.child_name.choices = [(child.id, child.child_name) for child in ChildRecord.query.all()]
    if form.validate_on_submit():
        student = ChildRecord.query.filter_by(id=form.child_name.data).first()
        student.attendance = form.attendance.data
        db.session.commit()
        flash('Attendance marked successfully!', 'success')
        return redirect(url_for('main.admin_dashboard'))
    return render_template('mark_attendance.html', title='Mark Attendance', form=form)

@main.route('/add_test', methods=['GET', 'POST'])
def add_test():
    form = AddTestForm()
    form.child_name.choices = [(child.id, child.child_name) for child in ChildRecord.query.all()]
    if form.validate_on_submit():
        student = ChildRecord.query.filter_by(id=form.child_name.data).first()
        student.test_score = form.test_score.data
        db.session.commit()
        flash('Test score added successfully!', 'success')
        return redirect(url_for('main.admin_dashboard'))
    return render_template('add_test.html', title='Add Test', form=form)

@main.route('/add_exam', methods=['GET', 'POST'])
def add_exam():
    form = AddExamForm()
    form.child_name.choices = [(child.id, child.child_name) for child in ChildRecord.query.all()]
    if form.validate_on_submit():
        student = ChildRecord.query.filter_by(id=form.child_name.data).first()
        student.exam_score = form.exam_score.data
        db.session.commit()
        flash('Exam score added successfully!', 'success')
        return redirect(url_for('main.admin_dashboard'))
    return render_template('add_exam.html', title='Add Exam', form=form)

@main.route('/add_classwork', methods=['GET', 'POST'])
def add_classwork():
    form = AddClassworkForm()
    form.child_name.choices = [(child.id, child.child_name) for child in ChildRecord.query.all()]
    if form.validate_on_submit():
        student = ChildRecord.query.filter_by(id=form.child_name.data).first()
        student.classwork_score = form.classwork_score.data
        db.session.commit()
        flash('Classwork score added successfully!', 'success')
        return redirect(url_for('main.admin_dashboard'))
    return render_template('add_classwork.html', title='Add Classwork', form=form)

@main.route('/add_homework', methods=['GET', 'POST'])
def add_homework():
    form = AddHomeworkForm()
    form.child_name.choices = [(child.id, child.child_name) for child in ChildRecord.query.all()]
    if form.validate_on_submit():
        student = ChildRecord.query.filter_by(id=form.child_name.data).first()
        student.homework_score = form.homework_score.data
        db.session.commit()
        flash('Homework score added successfully!', 'success')
        return redirect(url_for('main.admin_dashboard'))
    return render_template('add_homework.html', title='Add Homework', form=form)

# The Flask Logout
@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))  # Redirect to the login page or home page
