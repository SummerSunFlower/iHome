 # _*_ coding:utf-8 _*_
import functools

from flask import g
from flask import session, jsonify
from werkzeug.routing import BaseConverter

from iHome.utils.responce_code import RET


class RegexConverter(BaseConverter):
    def __init__(self,url_map,*args):
        super(RegexConverter, self).__init__(url_map)
        self.regex = args[0]


def login_required(func):

    # 防止装饰器去修改函数的名字
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # if 用户没有登录：
        user_id = session.get("user_id")
        if not user_id:
            return jsonify(errno=RET.SESSIONERR, errmsg="用户未登录")
        else:
            # 使用 g 变量去存储用户的id，在执行具体的视图函数的时候就可以不用再次去session中去取user_id
            g.user_id = user_id
            return func(*args, **kwargs)
    return wrapper
