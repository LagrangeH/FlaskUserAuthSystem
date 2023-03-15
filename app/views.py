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


@app.route('/')
def about():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email_raises = db.queries.is_email_registered(request.form.get('email'))
        username_raise = db.queries.is_username_registered(request.form.get('username'))

        if email_raises or username_raise:
            return render_template('auth/signup.html',
                                   email_raises=email_raises,
                                   username_raise=username_raise)

        password_hash = bcrypt.hashpw(request.form.get('password').encode('utf-8'), bcrypt.gensalt())

        new_user = db.models.User(
            username=request.form.get('username'),
            email=request.form.get('email'),
            password_hash=password_hash,
            registration_date=datetime.utcnow(),
        )

        db.queries.create_user(new_user)
        return render_template('index.html')

    return render_template('auth/signup.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        user = db.queries.get_user_by_email(request.form.get('email'))

        if user is None:
            return render_template('auth/signin.html', email_raise=True)

        if bcrypt.checkpw(request.form.get('password').encode('utf-8'), user.password_hash):
            session.clear()
            session['user_id'] = user.id
            return redirect('/')

        return render_template('auth/signin.html', password_raise=True)

    return render_template('auth/signin.html')


@app.route('/reset-password')
def reset_password():
    return render_template('auth/reset_password.html')


@app.route('/logout')
def logout():
    # session.clear()
    return redirect('/')


# TODO: Add restore_password view
