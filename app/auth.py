from ast import Pass
from flask import Blueprint, render_template, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, StringField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from markupsafe import Markup

auth = Blueprint("auth", __name__)

class LoginForm(FlaskForm):
    email = EmailField('Email address',validators=[InputRequired(), Email(), Length(min=3,max=255)])
    password = PasswordField('Password',validators=[InputRequired(), Length(min=8,max=100)])
    remember = BooleanField("Stay logged in")

class RegisterForm(FlaskForm):
    email = EmailField('Email address',validators=[InputRequired(), Email(), Length(min=3,max=255)])
    first_name = StringField('First name',validators=[InputRequired(), Length(max=35)])
    last_name = StringField('Last name',validators=[Length(max=35)])
    password = PasswordField('Password',validators=[InputRequired(), Length(min=8,max=100), EqualTo('password_confirm',message='Passwords do not match')])
    password_confirm = PasswordField('Confirm password')
    remember = BooleanField("Stay logged in")

@auth.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                flash(Markup("Logged in successfully!"),category='success')
                login_user(user, remember=form.remember.data)
                return redirect(url_for('views.home'))
            else:
                flash(Markup('Incorrect password.'),category='error')
    return render_template("login.html", user=current_user, form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
    
@auth.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print(form.email.data)
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash(Markup('User already exists'),'error')
            print('user exists')
        else:
            print('creating user')
            new_user = User(email=form.email.data,first_name=form.first_name.data,last_name=form.last_name.data,password=generate_password_hash(form.password.data,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=form.remember.data)
            flash(Markup('Account created'), category='success')
            return redirect(url_for("views.home"))
    print('refreshing page')
    return render_template("register.html",user=current_user, form=form)
    