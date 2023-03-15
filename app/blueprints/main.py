from flask import Blueprint, render_template

bp = Blueprint('main', __name__, url_prefix='/')


@bp.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404


@bp.route('/')
def about():
    return render_template('index.html')

