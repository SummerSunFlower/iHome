# _*_ coding:utf-8 _*_

from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from flask_migrate import Migrate,MigrateCommand,Manager

app = Flask(__name__)
manager = Manager(app)


class Config(object):
    SECRET_KEY = 'gsevorhwriogh4o3iht4i'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/iHome'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 配置redis
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    # 设置session保存参数
    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = 3600*24*100



app.config.from_object(Config)
db = SQLAlchemy(app)
redisstorge = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
CSRFProtect(app)
# 制定session保存的位置
Session(app)
Migrate(app,db)
manager.add_command("db",MigrateCommand)


@app.route('/', methods=['GET', "POST"])
def index():
    return "index"


if __name__ == "__main__":
    # 测试redis
    # redisstorge.set("name","laowang")
    # session['name'] = 'xiaohua'
    # app.run()
    manager.run()
