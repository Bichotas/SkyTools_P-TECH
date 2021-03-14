from app import app
from flask import Flask, render_template

@app.route('/')
def main():
    return render_template('blank.html')


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

