from aplicacion import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):

    __tablename__ = 'Cuentas'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), unique=False, nullable=False)
    image_profile = db.Column(db.String(20), unique=False, default='default.jpg')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_profile}')"


# Modelo para hcer la tabla en la base de datos

class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    complete = db.Column(db.Boolean)

    
    def __repr__(self):
        return f"Actividad('{self.text}', '{self.complete}')"

"""
class Tabla1(db.Model):

    __tablename__ = "tabla1"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=True)
    link = db.Column(db.String(100), unique=True, nullable=True)
    imagen_herramienta = db.Column(db.String(20), unique=False, default='profile_ex.jpg')

    def __repr__(self):
        return f"User('{self.__tablename__}', '{self.name}', '{self.imagen_herramienta}')"

class Tabla2(db.Model):

    __tablename__ = "tabla2"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=True)
    link = db.Column(db.String(100), unique=True, nullable=True)
    imagen_herramienta = db.Column(db.String(20), unique=False, default='profile_ex.jpg')

    def __repr__(self):
        return f"User('{self.__tablename__}', '{self.name}', '{self.imagen_herramienta}')"

class Tabla3(db.Model):

    __tablename__ = "tabla3"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=True)
    link = db.Column(db.String(100), unique=True, nullable=True)
    imagen_herramienta = db.Column(db.String(20), unique=False, default='profile_ex.jpg')

    def __repr__(self):
        return f"User('{self.__tablename__}', '{self.name}', '{self.imagen_herramienta}')"

class TablaGeneral(db.Model):

    __tablename__ = 'tablaGeneral'
    id = db.Column(db.Integer, primary_key=True)
    tabla1_id = db.Column(db.Integer, db.ForeignKey('tabla1.id'))
    tabla2_id = db.Column(db.Integer, db.ForeignKey('tabla2.id'))
    tabla3_id = db.Column(db.Integer, db.ForeignKey('tabla3.id'))"""