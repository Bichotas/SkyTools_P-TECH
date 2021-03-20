from flask import render_template, url_for, flash, redirect, request
from aplicacion.models import User
from aplicacion.forms import LoginForm, RegistrationForm
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

@app.route('/account')
@login_required
def account():
    return render_template('account.html')