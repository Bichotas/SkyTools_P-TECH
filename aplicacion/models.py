from aplicacion import db, login_manager
from flask_login import UserMixin
import os

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))

    def __repr__(self):
        return f"Actividad('{self.text}')"

class User(db.Model, UserMixin):

    __tablename__ = 'Cuentas'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), unique=False, nullable=False)
    image_profile = db.Column(db.String(20), unique=False, default='default.jpg')
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_profile}')"

