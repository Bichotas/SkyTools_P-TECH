import secrets
import os
from flask import render_template, url_for, flash, redirect, request
from aplicacion.models import User, Todo
from aplicacion.forms import LoginForm, RegistrationForm, UpdatingAccountForm, ActividadesInput
from aplicacion import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
def main():
    
    return render_template('blank.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main'))
        else:
            flash('Loggin unsuccesful. Please check you username and password', 'danger')
            
    return render_template('login.html', form=form)

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)
    return picture_fn



@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdatingAccountForm()
    image_file = url_for('static', filename='profile_pics/'+ current_user.image_profile)
    return render_template('profile.html', image_file=image_file, form=form)


# Ruta para actualizar datos 
@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    form = UpdatingAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_profile = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been udpated', 'success')
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/'+ current_user.image_profile)
    return render_template('update.html', image_file=image_file, form=form)


""" Version  1
class Actividades:
    def __init__(self, contenedor):
        self.contenedor = contenedor

    def cont(self):
        actividad = request.form['todoitem']
        self.contenedor = self.contenedor + "-" + actividad
        return self.contenedor
"""

""" Clase para input sin usar la clase wtf
class Actividades:

    def __init__(self, contenedor, strinV):
        self.contenedor = contenedor
        self.strinV = strinV


    def lista(self):
        inputo = request.form['todoitem']
        self.contenedor.append(inputo)
        return self.contenedor

    def cadena(self):
        self.strinV = "-".join(self.contenedor)
        return self.strinV
    """

""" Rutas para barra de herramientas """
@app.route('/uwu')
def index():
    incomplete = Todo.query.filter_by(complete=False).all()
    complete = Todo.query.filter_by(complete=True).all()

    #Parte con fumalrio wtf
    form = ActividadesInput()
    return render_template('index.html', incomplete=incomplete, complete=complete, form=form)

contenedor = []
string_V = ""
@app.route('/add', methods=['POST'])
def add():
    """todo = Todo(text=request.form['todoitem'], complete=False)
    db.session.add(todo)
    db.session.commit()"""

    #Parte sin flask-wtf
    """ctividadesBarra = Actividades(contenedor, string_V)
    lista_act =actividadesBarra.lista()
    fe_cadena = actividadesBarra.cadena()
    id_user = int(current_user.get_id())"""

    #Parte con formulario

    form = ActividadesInput()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            id_user = current_user.get_id()
            texto = form.text.data
            
        contenedor.append(texto)
        string_V = " - ".join(contenedor)
        todo = Todo(text=string_V, complete=False)
        db.session.add(todo)
        db.session.commit()
    print(contenedor)
    print(texto)
    print(string_V)
    # Parte en la que se agrega un campo por uno
    #todo = Todo(text=texto, complete=False)
    #id_user = current_user.get_id()
    #db.session.add(todo)
    #db.session.commit()
    #print(lista_act, fe_cadena, id_user)
    
    return redirect(url_for('index'))


@app.route('/complete/<id>')
def complete(id):

    todo = Todo.query.filter_by(id=int(id)).first()
    #Parte con el formulario
    form = ActividadesInput()
    todo.complete = True
    db.session.commit()
    return redirect(url_for('index'), form=form)

@app.route('/delete/<id>')
def delete(id):
    form = ActividadesInput()
    db.session.query(Todo).filter(Todo.id==id).delete()
    db.session.commit()

    return redirect(url_for('index'), form=form)

@app.route('/incomplete/<id>')
def incomplete(id):
    todo = Todo.query.filter_by(id=int(id)).first()
    form = ActividadesInput()
    todo.complete = False
    db.session.commit()

    return redirect(url_for('index'), form=form)

@app.route('/clear')
def clear():
    form = ActividadesInput()
    db.session.query(Todo).delete()
    db.session.commit()
    return redirect(url_for('index'), form=form)

