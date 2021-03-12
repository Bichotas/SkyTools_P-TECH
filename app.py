#Este va a ser el archivo para ejecutar la página
from flask import Flask, render_template
from flask_bootstrap import Bootstrap


app = Flask(__name__)
bootstrap = Bootstrap(app)
@app.route('/')
def index():
    return render_template('barraNavegación.html')


@app.route('/reg')
def register():
    return render_template('register.html')

@app.route('/nic')
def nice():
    return render_template('index.html')

if __name__== '__main__':
    app.run(debug=True)