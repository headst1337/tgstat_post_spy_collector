from flask import Blueprint

bp = Blueprint('scheduler', __name__, url_prefix='/api/v1')

from . import routes