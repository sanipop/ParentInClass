# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
#forms for Admin Function
class AddStudentForm(FlaskForm):
    child_name = StringField('Child Name', validators=[DataRequired()])
    submit = SubmitField('Add Student')

class MarkAttendanceForm(FlaskForm):
    child_name = SelectField('Child Name', choices=[], validators=[DataRequired()])
    attendance = SelectField('Attendance', choices=[('Present', 'Present'), ('Absent', 'Absent')], validators=[DataRequired()])
    submit = SubmitField('Mark Attendance')

class AddTestForm(FlaskForm):
    child_name = SelectField('Child Name', choices=[], validators=[DataRequired()])
    test_score = FloatField('Test Score', validators=[DataRequired()])
    submit = SubmitField('Add Test Score')

class AddExamForm(FlaskForm):
    child_name = SelectField('Child Name', choices=[], validators=[DataRequired()])
    exam_score = FloatField('Exam Score', validators=[DataRequired()])
    submit = SubmitField('Add Exam Score')

class AddClassworkForm(FlaskForm):
    child_name = SelectField('Child Name', choices=[], validators=[DataRequired()])
    classwork_score = FloatField('Classwork Score', validators=[DataRequired()])
    submit = SubmitField('Add Classwork Score')

class AddHomeworkForm(FlaskForm):
    child_name = SelectField('Child Name', choices=[], validators=[DataRequired()])
    homework_score = FloatField('Homework Score', validators=[DataRequired()])
    submit = SubmitField('Add Homework Score')
