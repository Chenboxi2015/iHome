from flask import Blueprint, session

api = Blueprint('api', __name__)
import index, verify_code
from ihome.models import *
