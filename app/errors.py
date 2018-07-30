from flask import (
    Blueprint, render_template
)

bp = Blueprint('errors', __name__, url_prefix='errors/')


@bp.app_errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 400

