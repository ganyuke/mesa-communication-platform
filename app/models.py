from . import db
from sqlalchemy.sql import func
from flask_login import UserMixin

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    author = db.Column(db.Integer, db.ForeignKey("user.id"))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    content = db.Column(db.Text)
    

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    author = db.Column(db.Integer, db.ForeignKey("user.id"))
    event_date = db.Column(db.DateTime(timezone=True), default=func.now())
    content = db.Column(db.Text)
    attendees = db.relationship("Attendee")


class Attendee(db.Model):
    __tablename__ = 'attendees'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique = True)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(255), unique = True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(35))
    last_name = db.Column(db.String(35))
    threads = db.relationship("Thread")
    