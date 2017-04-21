from flask import Blueprint

uye = Blueprint('uye', __name__)

from . import views
