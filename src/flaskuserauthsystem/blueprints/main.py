from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
def about():
    return render_template('index.html')


@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')
