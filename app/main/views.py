from flask import render_template,redirect,url_for,abort,request,flash
from app.main import main
from app.models import User,User_details,Comment,Subscriber
from .forms import Update,CreateUser_details
from .. import db
from flask_login import login_required,current_user
from ..email import mail_message
import secrets
import os
from PIL import Image  


@main.route('/')
def index():
    page = request.args.get('page',1, type = int )
    user_details = User_details.query.all()
    return render_template('index.html', user_details=user_details)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join('app/static/img', picture_filename)
    
    output_size = (200, 200)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_filename



@main.route('/profile',methods = ['POST','GET'])
@login_required
def profile():
    form = Update()
    if form.validate_on_submit():
        if form.profile_picture.data:
            picture_file = save_picture(form.profile_picture.data)
            current_user.profile_pic_path = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        db.session.commit()
        flash('Succesfully updated your profile')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
    profile_pic_path = url_for('static',filename = 'img/'+ current_user.profile_pic_path) 
    return render_template('profile/profile.html', profile_pic_path=profile_pic_path, form = form,user_details=user_details) 

@main.route('/user/<name>/update', methods = ['POST','GET'])
@login_required
def update(name):
    form = Update()
    user = User.query.filter_by(username = name).first()
    if user == None:
        abort(404)
    if form.validate_on_submit():
        user.bio = form.bio.data
        user.save()
        return redirect(url_for('.profile',name = name))
    return render_template('profile/update.html',form =form)



@main.route('/new_user_post', methods=['POST','GET'])
@login_required
def new_user_post(): 
    subscribers = Subscriber.query.all()
    form = CreateUser_details()
    if form.validate_on_submit():
        skills_title = form.skills_title.data
        description = form.description.data
        user_id =  current_user._get_current_object().id
        user_details = User_details(skills_title=skills_title,description=description,user_id=user_id)
        user_details.save()
        for subscriber in subscribers:
            mail_message("New skills post","email/new_skills",subscriber.email,user_details=user_details)
        return redirect(url_for('main.index'))
        flash('You posted a new skill')
        
    return render_template('new_post.html', form = form) 


@main.route('/user_details/<id>')
def user_details(id):
    comments = Comment.query.filter_by(user_details_id=id).all()
    user_details = User_details.query.get(id)
    return render_template('post.html',user_details=user_details,comments=comments) 



@main.route('/user_details/<user_details_id>/update', methods = ['GET','POST'])
@login_required
def update_user_details(user_details_id):
    user_details = User_details.query.get(user_details_id)
    if user_details.user != current_user:
        abort(403)
    form = CreateUser_details()
    if form.validate_on_submit():
        user_details.skills_title = form.skills_title.data
        user_details.description = form.description.data
        db.session.commit()
        flash("You have updated your Blog!")
        return redirect(url_for('main.user_details',id = user_details.id)) 
    if request.method == 'GET':
        form.skills_title_data = user_details.skills_title
        form.description.data = user_details.description
    return render_template('post.html', form = form) 



@main.route('/comment/<user_details_id>', methods = ['Post','GET'])
@login_required
def comment(user_details_id):
    user_details = User_details.query.get(user_details_id)
    comment =request.form.get('newcomment')
    new_comment = Comment(comment = comment, user_id = current_user._get_current_object().id, user_details_id=user_details_id)
    new_comment.save()
    return redirect(url_for('main.user_details',id = user_details.id)) 


def delete_comment(comment_id):
    if user_details.user != current_user:
        abort(403)
    comments = Comment.query.get(comment_id)
    comments.delete()
    flash("You have deleted your comment succesfully!")
    return redirect(url_for('main.user_details'))


@main.route('/subscribe',methods = ['POST','GET'])
def subscribe():
    email = request.form.get('subscriber')
    new_subscriber = Subscriber(email = email)
    new_subscriber.save_subscriber()
    mail_message("Subscribed to Techwise-Blog","email/welcome_subscriber",new_subscriber.email,new_subscriber=new_subscriber)
    flash('Sucessfuly subscribed')
    return redirect(url_for('main.index'))



@main.route('/user_details/<user_details_id>/delete', methods = ['POST'])
@login_required
def delete_post(user_details_id):
    user_details = User_details.query.get(user_details_id) 
    if user_details.user != current_user:
        abort(403)
    user_details.delete()
    flash("You have deleted your profile succesfully!")
    return redirect(url_for('main.index')) 


@main.route('/user/<string:username>')
def user_posts(username):
    user = User.query.filter_by(username=username).first()
    page = request.args.get('page',1, type = int )
    user_details = User_details.query.filter_by(user=user).order_by(User_details.posted.desc()).paginate(page = page, per_page = 4)
    return render_template('post.html',user_details=user_details,user = user)  