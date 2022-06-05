from ast import Pass
from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from .models import Thread
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, StringField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from markupsafe import Markup
import json

views = Blueprint('views', __name__)

class RegisterThread(FlaskForm):
    title = StringField('Title',validators=[InputRequired(), Length(max=35)])
    content = StringField('Body',validators=[InputRequired(), Length(max=35)])

@views.route("/stuff",methods=['GET','POST'])
def stuff():
    return render_template("stuff.html", user=current_user)

@views.route("/accountsetting.html",methods=['GET','POST'])
def accountsetting():
    return render_template("accountsetting.html", user=current_user)

@views.route("/",methods=['GET','POST'])
def home():
    form = RegisterThread()
    if form.validate_on_submit():
        if len(form.title.data) <= 1:
            flash(Markup('Make it longer!'),'error')
        else:
            new_thread = Thread(title=form.title.data,content=form.content.data,author=current_user.id)
            db.session.add(new_thread)
            db.session.commit()
            flash(Markup('Note added!'), category='success')
    return render_template("home.html", user=current_user,form=form)

@views.route('/delete-note',methods=['POST'])
def delete_note():
    thread = json.loads(request.data)
    thread_id = thread['noteId']
    thread = Thread.query.get(thread_id)
    if thread:
        if thread.author == current_user.id:
            db.session.delete(thread)
            db.session.commit()
    return jsonify({})