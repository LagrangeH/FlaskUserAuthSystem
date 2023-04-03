from flask import Blueprint, request, session, redirect, render_template
from flask_login import login_user, current_user, logout_user
from loguru import logger as log

from src.flaskuserauthsystem.database.recovery_link import RecoveryLink
from src.flaskuserauthsystem.database.user import User
from src.flaskuserauthsystem.utils.forms import RecaptchaForm
from src.flaskuserauthsystem.utils.password import hash_password, check_password
from src.flaskuserauthsystem.utils.mails import send_mail

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
        if request.form.get('password') != request.form.get('confirm_password'):
            log.debug('Passwords do not match')
            return render_template(
                'auth/signup.html',
                password_mismatch=True,
                form=form,
            )

        email_raises = User.is_email_registered(request.form.get('email'))
        username_raise = User.is_username_registered(request.form.get('username'))

        if email_raises or username_raise:
            return render_template(
                'auth/signup.html',
                email_raises=email_raises,
                username_raise=username_raise,
                form=form,
            )

        new_user = User(
            username=request.form.get('username'),
            email=request.form.get('email'),
            password_hash=hash_password(request.form.get('password')),
        )

        new_user.create()
        login_user(new_user)
        return redirect('/profile')

    return render_template('auth/signup.html', form=form)


@bp.route('/signin', methods=['GET', 'POST'])
def signin(form=None):
    if form is None:
        form = RecaptchaForm()

    if form.validate_on_submit():
        user = User.get_by_email(request.form.get('email'))

        if user is None:
            log.debug(f'User with email {request.form.get("email")} not found')
            return render_template('auth/signin.html', error=True, form=form)

        if check_password(request.form.get('password'), user.password_hash):
            session.clear()
            session['user_id'] = user.id
            login_user(user)
            return redirect('/')

        log.debug(f'Password for user {user} is incorrect')
        return render_template('auth/signin.html', error=True, form=form)

    return render_template('auth/signin.html', form=form)


@bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password(form=None):
    """
    TODO:
    [+] Создать таблицу с хэшами для восстановления пароля
        [+] Хэш должен быть уникальным
        [+] Хэш должен быть привязан к email
        [+] Хэш должен иметь время жизни
    [+] Создать функцию для генерации хэша
    [ ] Создать функцию для отправки письма с хэшем
    [ ] Создать функцию для проверки хэша
    [ ] Создать функцию для сброса пароля
    [ ] Создать функцию для отправки письма с новым паролем
    [+] Создать функцию для проверки времени жизни хэша
    [+] Создать функцию для удаления хэша
    [ ] Создать функцию для удаления всех хешей пользователя
    [ ] Удалить все хеши, когда пользователь авторизовался по существующему паролю или восстановил пароль
    [ ] Проверить, что запросов на восстановление пароля не больше 5 в день от одного email
    [ ] Написать тесты
    """
    if form is None:
        form = RecaptchaForm()

    if form.validate_on_submit():
        email = request.form.get('email')

        if not User.is_email_registered(email):
            log.debug(f'User with email {email} not found for password reset')
            return render_template('auth/reset_password.html', email_not_found=True, form=form)

        new_recovery_link = RecoveryLink(user_id=User.get_by_email(email).id)
        new_recovery_link.create()

        send_mail(recovery_link=new_recovery_link)

        return render_template('auth/check_email.html', email=email)

    return render_template('auth/reset_password.html', form=form)


@bp.route('/restore-password/<string:token>', methods=['GET', 'POST'])
def restore_password(token, form=None):
    """
    The form must be accessible by the hash generated
    after submitting the ``reset_password`` form.
    The hash link is sent to the specified email and is valid for some time
    """
    if form is None:
        form = RecaptchaForm()

    if form.validate_on_submit():
        # TODO
        log.debug('TODO')
        render_template('auth/signin.html', form=form)

    return render_template('auth/restore_password.html', form=form)


@bp.route('/signout')
def signout():
    logout_user()
    session.clear()
    return redirect('/')
