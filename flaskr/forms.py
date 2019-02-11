from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    k_number = StringField('k-number', validators=[DataRequired(), Length(min=8, max=9)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField("Login")

class RegistrationForm(FlaskForm):
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    k_number = StringField('k-number', validators=[DataRequired(), Length(min=8, max=9)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")
