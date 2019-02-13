from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    k_number = StringField('k-number', validators=[DataRequired(), Length(min=8, max=9)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    login_submit = SubmitField("Login")

class RegistrationForm(FlaskForm):
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    k_number = StringField('k-number', validators=[DataRequired(), Length(min=8, max=9)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired(), EqualTo("password")])
    registration_submit = SubmitField("Sign Up")
