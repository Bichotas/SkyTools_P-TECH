#Este va a ser el archivo para ejecutar la página
from flask import Flask, render_template
from flask_bootstrap import Bootstrap


app = Flask(__name__)
bootstrap = Bootstrap(app)


from routes import *


if __name__== '__main__':
    app.run(debug=True)