# _*_ coding:utf-8 _*_

import redis


class Config(object):
    SECRET_KEY = 'gsevorhwriogh4o3iht4i'
    #DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/iHome'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 配置redis
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    # 设置session保存参数
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = 3600 * 24 * 100


class DevelopmentConig(Config):
    DEBUG = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/iHome5'


config = {
    'DevelopmentConig':DevelopmentConig,
    'ProductionConfig':ProductionConfig
}

