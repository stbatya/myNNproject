"""Module contains functions that
define routes related to authorisation process
"""


from flask import Blueprint, flash
from flask import render_template, request, jsonify, redirect, url_for
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from webapp import db
from .models import User


#Setting a flask blueprint.
auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    """Route for login page"""
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    """Route for post from a login page"""

    #Form fields is written into respective variables.
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    #Making a query that will return user with the email from form
    #or none if there is no such user.
    user = User.query.filter_by(email=email).first()

    #If user doesn't exist or password is incorrect
    #than return a message using flash.
    if not user or not check_password_hash(user.password, password):
        flash('Incorrect email or password')
        return redirect(url_for('auth.login'))

    #If user with accepted email and passowrd is right than log user in.
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    """Route for sign up page"""
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    """Route for post from sign up page"""

    #Form fields is written into respective variables.
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()

    #Check if user exists. If so, return a message using flash.
    if user:
        flash('email already exists')
        return redirect(url_for('auth.signup'))

    #Insert a row into User table in db with recieved parameters.
    new_user = User(
            email=email, name=name,
            password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()

    #Redirect to login page.
    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    """Route for logout button"""
    logout_user()
    return redirect(url_for('main.index'))
