import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, DateField, \
    RadioField, SelectMultipleField
from wtforms.validators import DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    scheme_id = SelectField('Scheme', coerce=int)
    k_number = StringField('K-number', validators=[DataRequired(), Length(min=8, max=9)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    login_submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    scheme_id = SelectField('Scheme', coerce=int)
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    k_number = StringField('K-number', validators=[DataRequired(), Length(min=8, max=9)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo("password")])
    is_mentor = BooleanField('Is Mentor')
    registration_submit = SubmitField("Sign Up")


class RequestEmailPasswordResetForm(FlaskForm):
    scheme_id = SelectField('Scheme', coerce=int)
    k_number = StringField('K-number', validators=[DataRequired(), Length(min=8, max=9)])
    request_reset_password_submit = SubmitField("Send me an email")


class ResetPasswordWithEmailForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm New Password', validators=[
                                     DataRequired(), EqualTo("password")])
    reset_password_submit = SubmitField("Reset Password")


class ResetPasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired(), Length(min=8)])
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm New Password', validators=[
                                     DataRequired(), EqualTo("password")])
    reset_password_submit = SubmitField("Reset Password")


class NewSchemeForm(FlaskForm):
    scheme_name = StringField('Scheme Name', validators=[DataRequired()])
    year = IntegerField('Year Of Start', default=datetime.datetime.now().year,
                        validators=[DataRequired()])
    k_number = StringField('Scheme Admin K Number', validators=[
                           DataRequired(), Length(min=8, max=9)])
    submit = SubmitField('Create New Scheme')


class SystemLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField("Login")


class NewHobbyForm(FlaskForm):
    hobby_name = StringField('Hobby Name', validators=[DataRequired()])
    hobby_submit = SubmitField("Add new hobby")

class DeleteHobbyForm(FlaskForm):
    hobby = SelectField('Current Hobbies', coerce=int)
    submit = SubmitField("Remove Hobby")

class NewInterestForm(FlaskForm):
    interest_name = StringField('Interest Name', validators=[DataRequired()])
    interest_submit = SubmitField("Add new interest")

class DeleteInterestForm(FlaskForm):
    interest = SelectField('Current Interests', coerce=int)
    submit = SubmitField("Remove Interest")

class UserPreferencesForm(FlaskForm):
    gender = RadioField('Gender', choices=[], validators=[DataRequired()])
    date_of_birth = DateField('Date Of Birth')
    buddy_limit = IntegerField('Buddy Limit', validators=[DataRequired()])
    hobbies = SelectMultipleField('Hobbies', choices=[], coerce=int)
    interests = SelectMultipleField('Academic Interests', choices=[], coerce=int)
    user_preferences_submit = SubmitField('Submit')


class AllocationConfigForm(FlaskForm):
    age_weight = IntegerField('Age Weight')
    gender_weight = IntegerField('Gender Weight')
    hobby_weight = IntegerField('Hobby Weight')
    interest_weight = IntegerField('Interest Weight')
    allocation_config_submit = SubmitField("Update")

class SchemeFeedbackForm(FlaskForm):
    feedback_form_url = StringField('Feedback Form URL', validators=[DataRequired()])
    feedback_submit = SubmitField("Send")

class InviteForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField("Send")
