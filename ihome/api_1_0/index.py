# -*- coding:utf8 -*-
from . import api
@api.route('/')
def index():
    # session['name'] = 'cnbox'
    return 'index'