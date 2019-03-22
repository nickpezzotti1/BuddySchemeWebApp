from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, DateField, RadioField, SelectMultipleField
from wtforms.validators import DataRequired, Length, EqualTo
import datetime

class LoginForm(FlaskForm):
    scheme_id = SelectField('Scheme', coerce=int)
    k_number = StringField('k-number', validators=[DataRequired(), Length(min=8, max=9)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    login_submit = SubmitField("Login")

class RegistrationForm(FlaskForm):
    scheme_id = SelectField('Scheme', coerce=int)
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    k_number = StringField('k-number', validators=[DataRequired(), Length(min=8, max=9)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired(), EqualTo("password")])
    is_mentor = BooleanField('is_mentor')
    registration_submit = SubmitField("Sign Up")

class RequestPasswordResetForm(FlaskForm):
    scheme_id = SelectField('Scheme', coerce=int)
    k_number = StringField('k-number', validators=[DataRequired(), Length(min=8, max=9)])
    request_reset_password_submit = SubmitField("Send me an email")

class ResetPasswordForm(FlaskForm): ## scheme_id?
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired(), EqualTo("password")])
    reset_password_submit = SubmitField("Reset Password")

class NewSchemeForm(FlaskForm):
    scheme_name = StringField('Scheme Name', validators=[DataRequired()])
    year = IntegerField('Year Of Start', default=datetime.datetime.now().year, validators=[DataRequired()])
    k_number = StringField('Scheme Admin K Number', validators=[DataRequired(), Length(min=8, max=9)])
    submit = SubmitField('Create New Scheme')
    
class SystemLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField("Login")

class NewHobbyForm(FlaskForm):
    hobby_name = StringField('Hobby Name', validators=[DataRequired()])
    hobby_submit = SubmitField("Add new hobby")

class NewInterestForm(FlaskForm):
    interest_name = StringField('Interest Name', validators=[DataRequired()])
    interest_submit = SubmitField("Add new interest")

class MentorPreferencesForm(FlaskForm):
    gender = RadioField('Gender', choices=[])
    date_of_birth = DateField('Date Of Birth')
    buddy_limit = IntegerField('Buddy Limit')
    hobbies = SelectMultipleField('Hobbies', choices=[], coerce=int)
    interests = SelectMultipleField('Academic Interests', choices=[], coerce=int)
    user_preferences_submit = SubmitField('Submit')

    
