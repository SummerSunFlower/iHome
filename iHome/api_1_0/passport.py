# -*- coding:utf-8 -*-
# 实现登录和注册的逻辑
import re
from flask import current_app
from flask import request, jsonify
from flask import session

from iHome import redisstorge, db
from iHome.models import User
from iHome.utils.responce_code import RET

from . import api



@api.route('/users', methods=["POST"])
def register():
    """
    注册逻辑
    1. 获取参数：手机号, 短信验证码, 密码,
    2. 取到真实的短信验证码
    3. 进行验证码的对比
    4. 初始化User模型，保存相关数据
    5. 将user模型存到数据库中
    6. 给出响应：{"errno": "0", "errmsg": "注册成功"}
    :return:
    """

    # 1. 获取参数：手机号, 短信验证码, 密码,
    data_dict = request.json
    mobile = data_dict.get("mobile")
    phonecode = data_dict.get("phonecode")
    password = data_dict.get("password")
    # 判断参数是否都有值
    if not all([mobile, phonecode, password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 2. 取到真实的短信验证码
    try:
        real_phonecode = redisstorge.get("Mobile:" + mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询短信验证码失败")

    if not real_phonecode:
        return jsonify(errno=RET.NODATA, errmsg="短信验证码过期")

    # 3. 进行验证码的对比
    if phonecode != real_phonecode:
        return jsonify(errno=RET.DATAERR, errmsg="短信验证码输入错误")

    # 4. 初始化User模型，保存相关数据
    user = User()
    user.mobile = mobile
    user.name = mobile
    user.password = password

    # 5. 将user模型存到数据库中
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存用户数据失败")
    # 6. 给出响应：{"errno": "0", "errmsg": "注册成功"}
    return jsonify(errno=RET.OK, errmsg="注册成功")



@api.route('/session', methods=["POST"])
def login():
    """
    登录逻辑
    1. 获取参数
    2. 校验参数
    3. 通过mobile查询到指定的用户
    4. 校验密码
    5. 把当前用户相关登录信息保存到session中
    6. 返回
    :return:
    """

    # 1. 获取参数
    data_dict = request.json
    mobile = data_dict.get("mobile")
    password = data_dict.get("password")
    # 2. 校验参数
    if not all([mobile, password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 校验手机号是否正确
    if not re.match("^1[34578][0-9]{9}$", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="请输入正确的手机号")

    # 3. 通过mobile查询到指定的用户
    try:
        user = User.query.filter(User.mobile == mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据查询失败")

    if not user:
        return jsonify(errno=RET.USERERR, errmsg="当前用户不存在")

    # 4. 校验密码
    if not user.check_password(password):
        return jsonify(errno=RET.PWDERR, errmsg="密码错误")

    # 5. 保存用户信息到sessoin中
    session["user_id"] = user.id
    session["name"] = user.name
    session["mobile"] = user.mobile

    # 6. 给出响应
    return jsonify(errno=RET.OK, errmsg="登录成功")

