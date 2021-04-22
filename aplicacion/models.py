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
    category = db.Column(db.String(30), unique=False, nullable=False)
    image_tool = db.Column(db.String(20), unique=False, nullable=True)

    #Para hacer relacion en la tabla intermedia

    tool = db.relationship('Tool', backref='tool')


""" Tabla Intermedia para la funcion de agregar a favoritos la herramienta """

# Para mostrar todo y que hay una buena representación, se necestitará usar un Join, para sacar la informacion de dos tablas o más que es para lo que sirve
class User_Tool(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tool_id = db.Column(db.Integer, db.ForeignKey('tool.id'))