from re import A
import secrets
import os

from flask import render_template, url_for, flash, redirect, request, g
from flask.globals import session
from aplicacion.models import User, Activity, UserTool, Category, Tool
from aplicacion.forms import LoginForm, RegistrationForm, UpdatingAccountForm, ActividadesInput
from aplicacion import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime


fecha = datetime.now()

def addon(lista, nuevo):
    aux = lista[0]
    if nuevo == 'main' or nuevo == 'about' or nuevo == 'profile' or nuevo == 'account' or nuevo == 'chatbot' or nuevo == 'index' or nuevo == 'tools' or nuevo == 'learn' or nuevo == 'diagramas':
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
    myTools = db.session.query(Tool).select_from(UserTool).filter_by(users_id=id_user).join(Tool, UserTool.tool_id==Tool.id).all()
    """myTools = UserTool.query.filter_by(users_id=id_user).all()"""
    image_file = url_for('static', filename='profile_pics/'+ current_user.image_profile)
    return render_template('profile_new.html', image_file=image_file, form=form, a=a, incomplete=activities, myTools=myTools)


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

""" Rutas para barra de herramientas """
@app.route('/uwu')
def index():
    id_user = current_user.get_id()
    activities = Activity.query.filter_by(users_id=id_user).all()
    #Parte con fumalrio wtf
    myTools = Tool.query.filter_by(category=7).all()
    form = ActividadesInput()
    image_file = url_for('static', filename='profile_pics/'+ current_user.image_profile)
    return render_template('profile_new.html', incomplete=activities, form=form, image_file=image_file, myTools=myTools)

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



""" Funcion agregar herramientas a favoritos """

@app.route('/favorito/<id>')
def favorite(id):
    id_user = current_user.get_id()
    follana = g.lista_dou 
    form = ActividadesInput()
    sad = UserTool(users_id=id_user, tool_id=id)
    db.session.add(sad)
    db.session.commit()
    return redirect(url_for('account'))

    


@app.route('/tools')
def tools():
    
    #isa = ["a", "dos", "tres", "cuatro", "cinco,", "ses", "luis", "angeles", "barcelona", "nebula", "harder"]
    form = ActividadesInput()
    id_user = current_user.get_id()
    activities = Activity.query.filter_by(users_id=id_user).all()
    #myCategory = Category.query.all()
    myCategory = Category.query.filter_by(type_category_id=1).all()
    return render_template('tools.html',form=form, myCategory=myCategory, incomplete=activities)

@app.route('/learn')
def learn():
    
    #isa = ["a", "dos", "tres", "cuatro", "cinco,", "ses", "luis", "angeles", "barcelona", "nebula", "harder"]
    form = ActividadesInput()
    id_user = current_user.get_id()
    activities = Activity.query.filter_by(users_id=id_user).all()
    myCategory = Category.query.filter_by(type_category_id=2).all()
    return render_template('learn.html',form=form, myCategory=myCategory, incomplete=activities)

""" Funcion para checar descripcion de la herramienta """ 

"""@app.route('/<id>&<name>&<link>&<image_tool>&<image_preview>/<type_t>')
def check_description(id, name, link, image_tool, image_preview, type_t):
    form = ActividadesInput()
    id_tool = id
    name = name
    link = link
    image_tool = image_tool
    image_preview = image_preview
    type_t=type_t
    return render_template('check_description.html', name=name, form=form)

"""
@app.route('/<name>/<id>')
def check_description(name, id):
    form = ActividadesInput()
    id_user = current_user.get_id()
    activities = Activity.query.filter_by(users_id=id_user).all()

    # Parte para mostrar la pagina check
    desc = db.session.query(Tool).filter_by(id=id).first()
    image_tool = url_for('static', filename='image_tools/'+desc.image_tool)
    image_preview = url_for('static', filename='image_tools/'+desc.image_preview)
    return render_template('check_description.html',\
         incomplete=activities,\
         desc=desc, form=form,\
         image_tool=image_tool,\
         image_preview=image_preview)

""" Rutas para las categorías de Herramientas en la tabla "Category" """

@app.route('/diagramas')
def diagramas():
    form = ActividadesInput()
    id_user = current_user.get_id()
    activities = Activity.query.filter_by(users_id=id_user).all()
    myTools = Tool.query.filter_by(category=1).all()
    return render_template('categorias/Herramientas/diagramas.html', form=form, incomplete=activities, myTools=myTools)

@app.route('/mapas_mentales')
def mapas_mentales():
    form = ActividadesInput()
    id_user = current_user.get_id()
    activities = Activity.query.filter_by(users_id=id_user).all()
    myTools = Tool.query.filter_by(category=2).all()
    return render_template('categorias/Herramientas/mapas_mentales.html', form=form, incomplete=activities, myTools=myTools)

@app.route('/PDF_tools')
def pdf_tools():
    form = ActividadesInput()
    id_user = current_user.get_id()
    activities = Activity.query.filter_by(users_id=id_user).all()
    myTools = Tool.query.filter_by(category=3).all()
    return render_template('categorias/Herramientas/pdf_tools.html', form=form, incomplete=activities, myTools=myTools)

@app.route('/presentaciones')
def presentaciones():
    form = ActividadesInput()
    id_user = current_user.get_id()
    activities = Activity.query.filter_by(users_id=id_user).all()
    myTools = Tool.query.filter_by(category=4).all()
    return render_template('categorias/Herramientas/presentaciones.html', form=form, incomplete=activities, myTools=myTools)

@app.route('/line_time')
def line_time():
    form = ActividadesInput()
    id_user = current_user.get_id()
    activities = Activity.query.filter_by(users_id=id_user).all()
    myTools = Tool.query.filter_by(category=9).all()
    return render_template('categorias/Herramientas/lineas_de_tiempo.html', form=form, incomplete=activities, myTools=myTools)

@app.route('/editores_imagenes')
def editores_imagenes():
    form = ActividadesInput()
    id_user = current_user.get_id()
    activities = Activity.query.filter_by(users_id=id_user).all()
    myTools = Tool.query.filter_by(category=6).all()
    return render_template('categorias/Herramientas/editores_imagenes.html', form=form, incomplete=activities, myTools=myTools)
@app.route('/extensiones')
def extensiones():
    form = ActividadesInput()
    id_user = current_user.get_id()
    activities = Activity.query.filter_by(users_id=id_user).all()
    myTools = Tool.query.filter_by(category=7).all()
    return render_template('categorias/Herramientas/extensiones.html', form=form, incomplete=activities, myTools=myTools)

@app.route('/board_online')
def board_online():
    form = ActividadesInput()
    id_user = current_user.get_id()
    activities = Activity.query.filter_by(users_id=id_user).all()
    myTools = Tool.query.filter_by(category=8).all()
    return render_template('categorias/Herramientas/online_boards.html', form=form, incomplete=activities, myTools=myTools)


@app.route('/esquemas')
def esquemas():
    form = ActividadesInput()
    id_user = current_user.get_id()
    activities = Activity.query.filter_by(users_id=id_user).all()
    myTools = Tool.query.filter_by(category=10).all()
    return render_template('categorias/Herramientas/esquemas.html', form=form, incomplete=activities, myTools=myTools)

""" Rutas para las categorías Aprendizje en la tabla "Category" """

@app.route('/paginas_web')
def paginas_web():
    form = ActividadesInput()
    id_user = current_user.get_id()
    activities = Activity.query.filter_by(users_id=id_user).all()
    myTools = Tool.query.filter_by(category=2).all()
    return render_template('categorias/Aprendizaje/paginas_web.html', form=form, incomplete=activities, myTools=myTools)




