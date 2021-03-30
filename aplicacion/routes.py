import secrets
import os

from flask import render_template, url_for, flash, redirect, request, g
from aplicacion.models import User, Todo
from aplicacion.forms import LoginForm, RegistrationForm, UpdatingAccountForm, ActividadesInput
from aplicacion import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
def main():
    incomplete = Todo.query.filter_by().all()
    form = ActividadesInput()
    return render_template('blank.html', incomplete=incomplete, form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = RegistrationForm()
    if form.validate_on_submit():
        id_user = current_user.get_id()
        esp_blanco = db.session.query(Todo).filter(Todo.id == id_user).first()
        if esp_blanco == None:
            blanco = Todo(text="")
            db.session.add(blanco)
            db.session.commit()
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
    incomplete = Todo.query.filter_by().all()
    form = ActividadesInput()
    return render_template('about.html', incomplete=incomplete, form=form)


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
    incomplete = Todo.query.filter_by().all()
    form = ActividadesInput()
    a = UpdatingAccountForm()
    image_file = url_for('static', filename='profile_pics/'+ current_user.image_profile)
    return render_template('profile.html', image_file=image_file, form=form, a=a, incomplete=incomplete)


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

@app.route('/chatbot')
def chatbot():
    form = ActividadesInput()
    incomplete = Todo.query.filter_by().all()
    return render_template('chatbot.html', form=form, incomplete=incomplete)

""" Rutas para barra de herramientas """
@app.route('/uwu')
def index():
    incomplete = Todo.query.filter_by().all()
    #Parte con fumalrio wtf
    form = ActividadesInput()
    return render_template('index.html', incomplete=incomplete, form=form)

contenedor = []
string_V = ""
a = app
@app.route('/add', methods=['POST'])
def add():
    #Parte con formulario
    form = ActividadesInput()
    usuario_actual = current_user.username
    id_user = current_user.get_id()
    esp_blanco = db.session.query(Todo).filter(Todo.id == id_user).first()
    print(esp_blanco)
    if current_user.is_authenticated:
        if form.validate_on_submit():
            id_user = current_user.get_id()
            texto = form.text.data
            contenedor.append(texto)
            string_V = " - ".join(contenedor)
            barra = db.session.query(Todo).filter(Todo.id == id_user).update(
                {
                    Todo.text: string_V
                }
            )
            db.session.commit()
    return redirect(url_for('main'))
    

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
    db.session.commit()

    return redirect(url_for('index'), form=form)

@app.route('/clear')
def clear():
    form = ActividadesInput()
    db.session.query(Todo).delete()
    db.session.commit()
    return redirect(url_for('index'), form=form)    