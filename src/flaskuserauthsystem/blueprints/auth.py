import bcrypt
from flask import Blueprint, request, session, redirect, render_template
from flask_login import login_user, current_user
from loguru import logger as log

from src.flaskuserauthsystem.database import models, queries
from src.flaskuserauthsystem.utils.forms import RecaptchaForm


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/')
def auth():
    if current_user.is_authenticated:
        return redirect('/')
    return redirect('/auth/signup')


@bp.route('/signup', methods=['GET', 'POST'])
def signup(form=None):
    if form is None:
        form = RecaptchaForm()

    if form.validate_on_submit():
        email_raises = queries.is_email_registered(request.form.get('email'))
        username_raise = queries.is_username_registered(request.form.get('username'))

        if email_raises or username_raise:
            return render_template(
                'auth/signup.html',
                email_raises=email_raises,
                username_raise=username_raise,
                form=form
            )

        password_hash = bcrypt.hashpw(
            request.form.get('password').encode('utf-8'),
            bcrypt.gensalt()
        )

        new_user = models.User(
            username=request.form.get('username'),
            email=request.form.get('email'),
            password_hash=password_hash,
        )

        queries.create_user(new_user)
        login_user(new_user)
        return redirect('/')

    return render_template('auth/signup.html', form=form)


@bp.route('/signin', methods=['GET', 'POST'])
def signin(form=None):
    if form is None:
        form = RecaptchaForm()

    if form.validate_on_submit():
        user = queries.get_user_by_email(request.form.get('email'))

        if user is None:
            log.debug(f'User with email {request.form.get("email")} not found')
            return render_template('auth/signin.html', error=True, form=form)

        if bcrypt.checkpw(request.form.get('password').encode('utf-8'), user.password_hash):
            session.clear()
            session['user_id'] = user.id
            login_user(user)
            return redirect('/')

        log.debug(f'Password for user {user} is incorrect')
        return render_template('auth/signin.html', error=True, form=form)

    return render_template('auth/signin.html', form=form)


@bp.route('/reset-password')
def reset_password(form=None):
    if form is None:
        form = RecaptchaForm()

    if form.validate_on_submit():
        pass    # TODO: send email with hash link

    return render_template('auth/reset_password.html', form=form)


@bp.route('/restore-password', methods=['GET', 'POST'])
def restore_password(form=None):
    """
    The form must be accessible by the hash generated
    after submitting the ``reset_password`` form.
    The hash link is sent to the specified email and is valid for some time
    """
    if form is None:
        form = RecaptchaForm()

    if form.validate_on_submit():
        pass    # TODO: complete the view

    return render_template('auth/reset_password.html', form=form)


@bp.route('/signout')
def signout():
    session.clear()
    return redirect('/')
