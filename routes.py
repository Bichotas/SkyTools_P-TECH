
#Importamos del archivo app, el objeto app
from app import app
#Importamos los modulos y paquetes
from flask import Flask, render_template


#Ruta principal
@app.route('/')
def main():

    #Se retorna usando la funcion render template, la plantilla blank, la cual se usa para hacer pruebas xD
    return render_template('blank.html')


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

