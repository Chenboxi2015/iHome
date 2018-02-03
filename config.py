# -*- coding:utf8 -*-
class Config(object):
    """基本配置参数"""
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@127.0.0.1:8889/ihome"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopConfig(Config):
    DEBUG = True


class PromotionConfig(Config):
    pass


config_dict = {
    'develop': DevelopConfig,
    'promotion': PromotionConfig
}
