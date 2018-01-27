# _*_ coding:utf-8 _*_

from flask import Flask

app = Flask(__name__)


class Config(object):
    DEBUG = True

app.config.from_object(Config)


@app.route('/')
def index():
    return "index"

if __name__ == "__main__":
    app.run()
