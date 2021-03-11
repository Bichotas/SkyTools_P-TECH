#Este va a ser el archivo para ejecutar la página
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('barraNavegación.html')


if __name__== '__main__':
    app.run()