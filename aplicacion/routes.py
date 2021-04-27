from re import A
import secrets
import os

from flask import render_template, url_for, flash, redirect, request, g
from flask.globals import session
from aplicacion.models import User, Activity, UserTool, Category
from aplicacion.forms import LoginForm, RegistrationForm, UpdatingAccountForm, ActividadesInput
from aplicacion import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime


fecha = datetime.now()

def addon(lista, nuevo):
    aux = lista[0]
    if nuevo == 'main' or nuevo == 'about' or nuevo == 'profile' or nuevo == 'account' or nuevo == 'chatbot' or nuevo == 'index' or nuevo == 'tools':
        lista[0] = nuevo

    lista[1] = aux
    return lista




lista = ["",""]


@app.before_request
def before_request():
    new = request.endpoint
    print(new)
    g.lista_dou = addon(lista, new)
    print(g.lista_dou)

     
@app.route('/')
def main():
    id_user = current_user.get_id()
    activities = Activity.query.filter_by(users_id=id_user).all()
    form = ActividadesInput()
    return render_template('home.html', incomplete=activities, form=form)

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
    id_user = current_user.get_id()
    activities = Activity.query.filter_by(users_id=id_user).all()
    form = ActividadesInput()
    return render_template('about.html', incomplete=activities, form=form)


@app.route('/profile')
def profile():
    id_user = current_user.get_id()
    activities = Activity.query.filter_by(users_id=id_user).all()
    myCategory = Category.query.all()
    return render_template('profile.html', incomplete=activities, myCategory=myCategory)

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
    id_user = current_user.get_id()
    activities = Activity.query.filter_by(users_id=id_user).all()
    form = ActividadesInput()
    a = UpdatingAccountForm()
    image_file = url_for('static', filename='profile_pics/'+ current_user.image_profile)
    return render_template('profile.html', image_file=image_file, form=form, a=a, incomplete=activities)


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
    id_user = current_user.get_id()
    activities = Activity.query.filter_by(users_id=id_user).all()
    return render_template('chatbot.html', form=form, incomplete=activities)

""" Rutas para barra de herramientas """
@app.route('/uwu')
def index():
    id_user = current_user.get_id()
    activities = Activity.query.filter_by(users_id=id_user).all()
    #Parte con fumalrio wtf
    form = ActividadesInput()
    return render_template('index.html', incomplete=activities, form=form)

@app.route('/add', methods=['POST'])
def add():
    follana = g.lista_dou 
    #Parte con formulario
    form = ActividadesInput()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            id_user = current_user.get_id()
            a_Z = form.text.data
            owo = Activity(users_id=id_user, text=a_Z)
            db.session.add(owo)
            db.session.commit()
    return redirect(url_for(follana[0]))
    
@app.route('/delete/<id>')
def delete(id):
    form = ActividadesInput()
    db.session.query(Activity).filter(Activity.id==id).delete()
    db.session.commit()
    follana = g.lista_dou 

    #return redirect(url_for('index'), form=form)
    return redirect(url_for(follana[0]))

@app.route('/clear')
def clear():
    id_user = current_user.get_id()
    form = ActividadesInput()
    db.session.query(Activity).filter(Activity.users_id==id_user).delete()
    db.session.commit()
    follana = g.lista_dou
    return redirect(url_for(follana[0]))
    
@app.route('/tools')
def tools():
    
    #isa = ["a", "dos", "tres", "cuatro", "cinco,", "ses", "luis", "angeles", "barcelona", "nebula", "harder"]
    form = ActividadesInput()
    id_user = current_user.get_id()
    activities = Activity.query.filter_by(users_id=id_user).all()
    myCategory = Category.query.all()
    return render_template('tools.html',form=form, myCategory=myCategory, incomplete=activities)


""" Rutas para las categorías en la tabla "Category" """

@app.route('/diagramas')
def diagramas():
    form = ActividadesInput()
    return render_template('blank.html', form=form)

@app.route('/mapas_mentales')
def mapas_mentales():
    form = ActividadesInput()
    return render_template('blank.html', form=form)

@app.route('/PDF_tools')
def pdf_tools():
    form = ActividadesInput()
    return render_template('blank.html', form=form)

@app.route('/presentaciones')
def presentaciones():
    form = ActividadesInput()
    return render_template('blank.html', form=form)

@app.route('/esquemas')
def esquemas():
    form = ActividadesInput()
    return render_template('blank.html', form=form)

@app.route('/editor_imagenes')
def editor_imagenes():
    form = ActividadesInput()
    return render_template('blank.html', form=form)

@app.route('/extensiones')
def extensiones():
    form = ActividadesInput()
    return render_template('blank.html', form=form)

