from flask import Blueprint
from flask import render_template, request, jsonify, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from webapp import db
from flask import flash
from flask_login import login_user
#from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash('Incorrect email or password')
        return redirect(url_for('auth.login'))
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html',flag=0)

@auth.route('/signup',methods=['POST'])
def signup_post():
    email = request.form.get('email')
    print(email)
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        print('exist!')
        flash('email already exists')
        return redirect(url_for('auth.signup',flag=1))
    new_user = User(email=email, name=name, password=generate_password_hash(password,method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))#after signup we redirect user to login page

@auth.route('/logout')
def logout():
    return 'Logout'
