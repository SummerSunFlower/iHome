 # _*_ coding:utf-8 _*_
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from config import Config


app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)
redisstorge = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
CSRFProtect(app)
# 制定session保存的位置
Session(app)
