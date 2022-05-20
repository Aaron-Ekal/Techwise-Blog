from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,TextAreaField, SubmitField,ValidationError
from wtforms.validators import InputRequired,Email
from flask_login import current_user
from ..models import User

class Update(FlaskForm):
    username = StringField('Enter Your Username', validators=[InputRequired()])
    email = StringField('Email Address', validators=[InputRequired(),Email()])
    bio = TextAreaField('Write a brief bio about you.',validators = [InputRequired()])
    profile_picture = FileField('profile picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def validate_email(self,email):
        if email.data != current_user.email:
            if User.query.filter_by(email = email.data).first():
                raise ValidationError("The Email has already been taken!")
    
    def validate_username(self, username):
        if username.data != current_user.username:
            if User.query.filter_by(username = username.data).first():
                raise ValidationError("The username has already been taken")

class CreateUser_details(FlaskForm):
    skills_title = StringField('Title',validators=[InputRequired()])
    description = TextAreaField('Write your skills post here',validators=[InputRequired()])
    charges = StringField('Charges') 
    contact = StringField('Contact', validators=[InputRequired()])
    submit = SubmitField('Post')  