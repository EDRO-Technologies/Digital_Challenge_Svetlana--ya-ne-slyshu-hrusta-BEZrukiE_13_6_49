from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    patronymic = StringField('Patronymic', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    submit_profile = SubmitField('Update Profile')

class AchievementForm(FlaskForm):
    achievements = TextAreaField('Achievements', validators=[DataRequired()])
    submit_achievement = SubmitField('Save Achievements')

class TakeOffForm(FlaskForm):
    preferences = StringField('Preferences', validators=[DataRequired()])
    submit = SubmitField('Generate Goals')