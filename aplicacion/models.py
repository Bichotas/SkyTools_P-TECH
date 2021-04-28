from aplicacion import db, login_manager
from flask_login import UserMixin
import os

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), unique=False, nullable=False)
    image_profile = db.Column(db.String(20), unique=False, default='default.jpg')
    activity = db.relationship('Activity', backref='user_ax')

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    text = db.Column(db.String(200))

class Tool(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    link = db.Column(db.String(220), unique=False, nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('category.id'))
    image_tool = db.Column(db.String(20), unique=False, nullable=True)
    tool = db.relationship('UserTool', backref='user_tool')


class UserTool(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tool_id = db.Column(db.Integer, db.ForeignKey('tool.id'))

class Category(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(20), unique=True, nullable=False)
    image_category = db.Column(db.String(30), unique=False, nullable=True)
    type_category_id = db.Column(db.Integer, db.ForeignKey('type.id'))
    url_for_category = db.Column(db.String(30), unique=True, nullable=True)
    category_rel = db.relationship('Tool', backref='category')

class Type(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name_type = db.Column(db.String(30), unique=True, nullable=False)
    type_ca = db.relationship('Category', backref='type_ca')


