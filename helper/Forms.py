from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField
from wtforms.validators import DataRequired, EqualTo, Length

class CreateUserForm(FlaskForm):
    fname = StringField(label='First Name: ', validators=[DataRequired(), Length(min=2)])
    lname = StringField(label='Last Name: ', validators=[DataRequired(), Length(min=2)])
    birthday = DateField(label='Date of Birth: ', validators=[DataRequired()])
    username = StringField(label='Create Username: ', validators=[DataRequired(), Length(min=6, max=12)])
    password = PasswordField(label='Create password: ', validators=[DataRequired(), Length(min=8, max=20)])
    password_confirmation = PasswordField(label='Confirm password: ', validators=[DataRequired(), EqualTo(fieldname='password', message='Passwords must match.')])
    submitBtn = SubmitField(label='Register')

class LoginForm(FlaskForm):
    username = StringField(label='Username: ', validators=[DataRequired()])
    password = PasswordField(label='Password: ', validators=[DataRequired()])
    submitBtn = SubmitField(label='Submit')