from flask import Blueprint, render_template
from flask_wtf.csrf import CSRFError


bp = Blueprint('main', __name__, url_prefix='/')


@bp.errorhandler(404)
def page_not_found():
    return render_template('errors/404.html'), 404


@bp.errorhandler(CSRFError)
def handle_csrf_error(error):
    return render_template('errors/csrf.html', reason=error.description), 400


@bp.route('/')
def about():
    return render_template('index.html')
