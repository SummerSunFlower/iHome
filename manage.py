# _*_ coding:utf-8 _*_

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis

app = Flask(__name__)


class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/iHome'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 配置redis
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379

app.config.from_object(Config)
db = SQLAlchemy(app)
redisstorge = redis.StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT)

@app.route('/')
def index():
    return "index"

if __name__ == "__main__":
    # 测试redis
    #redisstorge.set("name","laowang")
    app.run()
