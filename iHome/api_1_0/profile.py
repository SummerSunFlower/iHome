# -*- coding:utf-8 -*-
from flask import current_app, jsonify
from flask import g
from flask import request
from flask import session

from iHome import constants, db
from iHome.models import User
from iHome.utils.common import login_required
from iHome.utils.image_storage import upload_image
from iHome.utils.responce_code import RET

from . import api


@api.route('/user')
@login_required
def get_user_info():
    """
    获取用户信息
    0. TODO 判断当前用户是否登录
    1. 取到当前登录用户的id
    2. 查询出指定的用户信息
    3. 组织数据，进行返回
    :return:
    """

    # 1. 取到当前登录用户的id
    user_id = session.get("user_id")

    # 2. 查询出指定的用户信息
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据失败")

    if not user:
        return jsonify(errno=RET.NODATA, errmsg="用户不存在")

    # 3. 组织数据，进行返回
    resp = {
        "name": user.name,
        "avartar_url": user.avatar_url,
        "user_id": user.id
    }
    return jsonify(errno=RET.OK, errmsg="OK", data=user.to_dict())



@api.route('/user/avatar', methods=["POST"])
@login_required
def upload_avatar():
    """
    上传用户头像
    0. 判断用户是否登录
    1. 获取到上传的图片文件
    2. 判断图片文件是否存在
    3. 上传图片文件到七牛云
    4. 上传成功之后，保存到用户表的头像字段中
    5. 返回响应，带上头像地址
    :return:
    """

    # 1. 获取到上传的图片文件 / 2. 判断图片文件是否存在
    try:
        avatar_data = request.files.get("avatar").read()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg="请取文件失败")

    # 3. 上传图片文件到七牛云
    try:
        key = upload_image(avatar_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="上传图片失败")

    # 4. 上传成功之后，保存到用户表的头像字段中
    # user_id = session.get("user_id")
    user_id = g.user_id
    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据失败")

    if not user:
        return jsonify(errno=RET.NODATA, errmsg="用户不存在")

    # 设置值到用户模型身上数据
    user.avatar_url = key

    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="保存数据失败")

    # 5. 返回响应，带上头像地址
    avatar_url = constants.QINIU_DOMIN_PREFIX + key
    return jsonify(errno=RET.OK, errmsg="上传成功", data={"avatar_url": avatar_url})


@api.route('/user/name', methods=["POST"])
@login_required
def set_user_name():
    """
    修改用户名
    0. 判断用户是否登录
    1. 获取传过来的用户名，并判断是否有值
    2. 查询到当前登录用户
    3. 更新当前登录用户的模型
    4. 并保存到数据库
    5. 返回响应
    :return:
    """

    # 1. 获取传过来的用户名，并判断是否有值
    user_name = request.json.get("name")
    if not user_name:
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 2. 查询到当前登录用户
    # user_id = session.get("user_id")
    user_id = g.user_id

    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据出错")

    if not user:
        return jsonify(errno=RET.NODATA, errmsg="当前用户不存在")

    # 3. 更新当前登录用户的模型
    user.name = user_name

    # 4. 并保存到数据库
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="保存数据失败")
    # 更新session中保存的用户名
    session["name"] = user.name
    # 5. 返回响应
    return jsonify(errno=RET.OK, errmsg="保存成功")




@api.route('/user/auth', methods=["POST"])
@login_required
def set_user_auth():
    """
    设置用户实名认证信息
    1. 获取参数，并判断参数是有值
    2. 查询出当前用户的模型
    3. 更新模型
    4. 保存到数据库
    5. 返回响应
    :return:
    """
    pass

    # 1. 获取参数，并判断参数是有值
    data_dict = request.json
    real_name = data_dict.get("real_name")
    id_card = data_dict.get("id_card")

    if not all([real_name, id_card]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 2. 查询出当前用户的模型
    user_id = g.user_id

    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据失败")

    if not user:
        return jsonify(errno=RET.NODATA, errmsg="用户不存在")

    # 3. 更新模型
    user.real_name = real_name
    user.id_card = id_card

    # 4. 保存到数据库

    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="数据保存失败")

    # 5. 返回响应
    return jsonify(errno=RET.OK, errmsg="保存成功")

@api.route('/user/auth')
@login_required
def get_user_auth():
    """
    获取用户的实名认证信息
    :return:
    """
    # 1. 查询出当前用户的模型
    user_id = g.user_id

    try:
        user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据失败")

    if not user:
        return jsonify(errno=RET.NODATA, errmsg="用户不存在")

    # 2. 封装响应

    resp = {
        "real_name": user.real_name,
        "id_card": user.id_card
    }
    return jsonify(errno=RET.OK, errmsg="OK", data=resp)
