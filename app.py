#Este va a ser el archivo para ejecutar la página

#Importamos los modulos flask y render template

""" El render template se usa para poner plantillas o archivos html en flask"""
from flask import Flask, render_template

#Modulo de bootstrap
from flask_bootstrap import Bootstrap


#Inicializamos la aplicacion guardándola en una variable
app = Flask(__name__)

#Se hace un objeto con el modulo bootstrap, utilizando la aplicación ya anteriormente inicializada
bootstrap = Bootstrap(app)

#Se importa el archivo rutas, estoo para que se ejecuten como si estuviesen en este mismo archivo
from routes import *


#Ponemos "persistencia", esto para que detecte la aplicación que esta inicializada, esta la corra y ponga sus parametros
if __name__== '__main__':
    app.run(debug=True)