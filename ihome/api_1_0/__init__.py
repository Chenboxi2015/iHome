from flask import Blueprint, session

api = Blueprint('api', __name__)
import index, verify_code, password
from ihome.models import *
