from flask import render_template, url_for, flash, redirect
from aplicacion.models import User
from aplicacion.forms import LoginForm, RegistrationForm
from aplicacion import app

@app.route('/')
def main():
    return render_template('blank.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}', 'success')
        return redirect(url_for('main'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
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