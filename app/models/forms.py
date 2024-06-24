from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import Email, Length, InputRequired
from datetime import datetime

class RegForm(FlaskForm):
    email = StringField('Email',  validators=[InputRequired(message='This field is required.'), Email(message='Invalid email'), Length(max=30, message='Field cannot be longer than 30 characters.')])
    password = PasswordField('Password', validators=[InputRequired(message='This field is required.'), Length(min=5,max=20,message='Field must be between 5 and 20 characters long.')])
    name = StringField('Name')

class dtForm(FlaskForm):
    tee_time = DateTimeLocalField('Tee_time', validators=[InputRequired(message='This field is required.')], format='%Y-%m-%dT%H:%M')