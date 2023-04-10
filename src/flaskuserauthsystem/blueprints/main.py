from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
def about():
    if current_user.is_authenticated:
        return redirect('/profile')
    else:
        return redirect('/auth/signin')


@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')
