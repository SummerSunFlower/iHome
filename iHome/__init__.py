# _*_ coding:utf-8 _*_
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from config import config
from iHome.api_1_0 import api


db = SQLAlchemy()
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # db = SQLAlchemy(app)
    db.init_app(app)
    redisstorge = redis.StrictRedis(host=config[config_name].REDIS_HOST, port=config[config_name].REDIS_PORT)
    CSRFProtect(app)
    # 制定session保存的位置
    Session(app)
    from api_1_0 import api
    app.register_blueprint(api)
    print app.url_map
    return app
