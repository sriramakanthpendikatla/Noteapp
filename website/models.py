from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import datetime
from pytz import timezone


def get_ist_time():
    """Return current time in IST timezone"""
    ist = timezone('Asia/Kolkata')
    return datetime.datetime.now(ist)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=get_ist_time)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')


