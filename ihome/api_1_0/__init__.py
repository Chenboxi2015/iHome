from flask import Blueprint

api = Blueprint('api', __name__)
from . import *


@api.route('/')
def index():
    return 'index'
