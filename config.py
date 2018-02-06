# -*- coding:utf8 -*-
import redis


class Config(object):
    """基本配置参数"""
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@127.0.0.1:8889/ihome"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # post请求和session需要
    SECRET_KEY = 'AeHLwvUll230jVSRGZt5pbhX4zX+2oU='

    # redis
    REDIS_PORT = 6379
    REDIS_HOST = '127.0.0.1'

    # 配置session存储到redis中
    PERMANENT_SESSION_LIFETIME = 86400  # 单位是秒, 设置session过期的时间
    SESSION_TYPE = 'redis'  # 指定存储session的位置为redis
    SESSION_USE_SIGNER = True  # 对数据进行签名加密, 提高安全性 secret_key
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)  # 设置redis的ip和端口


class DevelopConfig(Config):
    DEBUG = True


class PromotionConfig(Config):
    pass


config_dict = {
    'develop': DevelopConfig,  # 开发模式
    'promotion': PromotionConfig  # 生成模式
}
