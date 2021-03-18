from flask import Flask, render_template, url_for, flash, redirect
from forms import LoginForm, RegistrationForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY']='5d0a9f096785838c292e4212b9deba2a'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)

class User(db.Model):

    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_profile = db.Column(db.String(20), unique=False, default='default.jpg')
    password = db.Column(db.String(60), unique=False, nullable=False)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_profile}')"

db.create_all()
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
if __name__== '__main__':
    app.run(debug=True)