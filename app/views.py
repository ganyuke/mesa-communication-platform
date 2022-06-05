from flask import Flask, Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('base.html',user=current_user)