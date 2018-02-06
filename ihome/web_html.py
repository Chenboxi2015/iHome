# -*- coding:utf8 -*-
from flask import Blueprint, current_app, make_response
from flask_wtf.csrf import generate_csrf

html = Blueprint('html', __name__)


@html.route('/<re(r".*"):file_name>')
def web_html(file_name):
    if not file_name:
        file_name = 'index.html'
    if file_name != 'favicon.ico':
        file_name = 'html/' + file_name
    # 设置csrf_token到cookie中 并会给session同步存储一份
    # 读取会从session中读取
    csrf_token = generate_csrf()
    response = make_response(current_app.send_static_file(file_name))
    response.set_cookie('csrf_token', csrf_token)
    return response

