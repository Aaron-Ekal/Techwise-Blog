from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import InputRequired,Email,EqualTo, Length
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[InputRequired()])
    password = PasswordField('Password',validators=[InputRequired()])
    remember = BooleanField('Remember Me!')
    submit = SubmitField('Login')

class SignUp(FlaskForm):
    username = StringField('Enter Your Username', validators=[InputRequired(), Length(min=4, max=20)])
    email = StringField('Email Address', validators=[InputRequired(),Email()])
    password = PasswordField('Password',validators = [InputRequired(), EqualTo('password_confirm',message = 'Passwords must match')])
    password_confirm = PasswordField('Confirm Passwords',validators = [InputRequired()])
    submit = SubmitField('Sign Up')

    def validate_email(self,data_field):
        if User.query.filter_by(email = data_field.data).first():
            raise ValidationError(message="The Email has already been taken!")
    
    def validate_username(self, data_field):
        if User.query.filter_by(username = data_field.data).first():
            raise ValidationError(message="The username has already been taken")