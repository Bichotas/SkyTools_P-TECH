from __main__ import db

class User(db.Model):

    __tablename__ = 'Cuentas'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), unique=False, nullable=False)
    image_profile = db.Column(db.String(20), unique=False, default='default.jpg')


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_profile}')"
