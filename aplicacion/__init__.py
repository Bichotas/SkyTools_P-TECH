from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SECRET_KEY']='5d0a9f096785838c292e4212b9deba2a'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)

from aplicacion import routes