from flask import Blueprint, render_template


bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/')
def about():
    return render_template('index.html')
