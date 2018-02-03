# -*- coding:utf8 -*-
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import config_dict

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    # 配置参数
    app.config.from_object(config_dict[config_name])
    db.init_app(app)

    # 注册蓝图
    from ihome.api_1_0 import api
    app.register_blueprint(api, url_prefix='/api/v1.0')
    return app, db
