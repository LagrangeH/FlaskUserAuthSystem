from datetime import datetime

import bcrypt
from flask import Blueprint, request, session, redirect, render_template
from loguru import logger as log

from database import models, queries


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/')
def auth():
    # TODO
    return "Auth root page"


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email_raises = queries.is_email_registered(request.form.get('email'))
        username_raise = queries.is_username_registered(request.form.get('username'))

        if email_raises or username_raise:
            return render_template('auth/signup.html',
                                   email_raises=email_raises,
                                   username_raise=username_raise)

        password_hash = bcrypt.hashpw(request.form.get('password').encode('utf-8'), bcrypt.gensalt())

        new_user = models.User(
            username=request.form.get('username'),
            email=request.form.get('email'),
            password_hash=password_hash,
            registration_date=datetime.utcnow(),
        )

        queries.create_user(new_user)
        return render_template('index.html')

    return render_template('auth/signup.html')


@bp.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        user = queries.get_user_by_email(request.form.get('email'))

        if user is None:
            log.debug(f'User with email {request.form.get("email")} not found')
            return render_template('auth/signin.html', email_raise=True)

        elif bcrypt.checkpw(request.form.get('password').encode('utf-8'), user.password_hash):
            session.clear()
            session['user_id'] = user.id
            return redirect('/')

        else:
            log.debug(f'Password for user {user} is incorrect')
            return render_template('auth/signin.html', password_raise=True)

    return render_template('auth/signin.html')


@bp.route('/reset-password')
def reset_password():
    return render_template('auth/reset_password.html')


@bp.route('/signout')
def signout():
    session.clear()
    return redirect('/')


# TODO: Add restore_password view