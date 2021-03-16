from flask import Flask, render_template, url_for, flash, redirect
from forms import LoginForm, RegistrationForm


app = Flask(__name__)
app.config['SECRET_KEY']='5d0a9f096785838c292e4212b9deba2a'

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

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__== '__main__':
    app.run(debug=True)