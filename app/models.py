from . import db,login_manager
from flask_login import current_user,UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id) 

class User (UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),unique = True,nullable = False)
    email = db.Column(db.String(255), unique = True,nullable = False)
    bio = db.Column(db.String(255),default ='My default Bio')
    profile_pic_path = db.Column(db.String(150),default ='default.png')
    hashed_password = db.Column(db.String(255),nullable = False)
    user_details = db.relationship('User_details', backref='user', lazy='dynamic')
    comment = db.relationship('Comment', backref='user', lazy='dynamic')
    
    @property
    def set_password(self):
        raise AttributeError('You cannot read the password attribute')

    @set_password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.hashed_password,password)

    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "User: %s" %str(self.username)

class User_details(db.Model):
    __tablename__ = 'user_details'
    id = db.Column(db.Integer,primary_key=True)
    skills_title = db.Column(db.String(255),nullable=False)
    description = db.Column(db.Text(),nullable=False)
    charges = db.Column(db.String) 
    contact = db.Column(db.String) 
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    comment = db.relationship('Comment', backref='user_details', lazy='dynamic')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_user_details(id): 
        user_details = user_details.query.filter_by(id=id).first()

        return user_details

    def __repr__(self):
        return f'user_details {self.skills_title}'

class Comment(db.Model):
    __tablename__='comments'

    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.String)
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_details_id = db.Column(db.Integer,db.ForeignKey("user_details.id"))
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_comment(id):
        comment = Comment.query.all(id=id)
        return comment


    def __repr__(self):
        return f'Comment {self.comment}'

class Subscriber(db.Model):
    __tablename__='subscribers'

    id=db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(255),unique=True,index=True)

    def save_subscriber(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'Subscriber {self.email}'