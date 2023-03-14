import functools
from datetime import datetime

import bcrypt
from flask import render_template, request, redirect, session, g
from loguru import logger as log

import db.models
import db.queries
from loader import app


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect('signin')

        return view(**kwargs)

    return wrapped_view


@app.route('/', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        content = request.form.to_dict()

        email_raises = db.queries.is_email_registered(content['email'])
        username_raise = db.queries.is_username_registered(content['username'])

        if email_raises or username_raise:
            return render_template('auth/signup.html',
                                   email_raises=email_raises,
                                   username_raise=username_raise)

        password_hash = bcrypt.hashpw(content['password'].encode('utf-8'), bcrypt.gensalt())

        new_user = db.models.User(
            username=content['username'],
            email=content['email'],
            password_hash=password_hash,
            registration_date=datetime.utcnow(),
        )

        db.queries.create_user(new_user)

    return render_template('index.html')


@app.route('/signup')
def signup():
    return render_template('auth/signup.html')


@app.route('/signin')
def signin():
    return render_template('auth/signin.html')


@app.route('/reset-password')
def reset_password():
    return render_template('auth/reset_password.html')


@app.route('/logout')
def logout():
    # session.clear()
    return redirect('/')
