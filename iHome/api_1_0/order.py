# -*- coding:utf-8 -*-
import datetime

from flask import current_app
from flask import g
from flask import request, jsonify

from iHome import db
from iHome.api_1_0 import api
from iHome.models import Order, House
from iHome.utils.common import login_required
from iHome.utils.responce_code import RET


@api.route('/orders/<order_id>', methods=["PUT"])
@login_required
def set_order_status(order_id):
    """
    设置订单状态
    1. order_id找到对应的订单
    2. 判断当前登录用户是否该订单对应房屋的房东
    3. 修改订单状态
    4. 保存数据库
    5. 返回响应
    :param order_id:
    :return:
    """

    # 1. order_id找到对应的订单
    try:
        order = Order.query.filter(Order.id == order_id, Order.status == "WAIT_ACCEPT").first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据错误")

    if not order:
        return jsonify(errno=RET.NODATA, errmsg="订单不存在")

    # 2. 判断当前登录用户是否该订单对应房屋的房东
    user_id = g.user_id
    # 取当前订单的房东的id
    landlord_id = order.house.user_id
    if user_id != landlord_id:
        return jsonify(errno=RET.ROLEERR, errmsg="不允许修改订单状态")

    # 3. 修改订单状态
    order.status = "WAIT_COMMENT"

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="修改订单状态失败")

    return jsonify(errno=RET.OK, errmsg="OK")


@api.route('/orders')
@login_required
def order_list():
    """
    获取当前登录用户<房客>的所有订单
    :return:
    """

    user_id = g.user_id
    role = request.args.get("role")  # 如果 role=landlord 代表查询房东的订单  如果是custom表示查询房客订单

    # 校验参数
    if not role:
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    if role not in("landlord", "custom"):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 查询数据
    try:
        if role == "landlord":
            # 查询作为房东的所有的订单
            houses = House.query.filter(House.user_id == user_id).all()
            # 获取到房屋的id
            houses_id = [house.id for house in houses]
            orders = Order.query.filter(Order.house_id.in_(houses_id)).all()
        elif role == "custom":
            # 查询作为房客的所有的订单
            orders = Order.query.filter(Order.user_id == user_id).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据失败")

    # 转成字典列表
    order_dict_li = []

    for order in orders:
        order_dict_li.append(order.to_dict())

    return jsonify(errno=RET.OK, errmsg="OK", data=order_dict_li)


@api.route("/orders", methods=["POST"])
@login_required
def create_order():
    """
    添加新订单
    1. 获取参数：房屋id，开始入住时间，结束入住时间
    2. 判断参数/校验参数
    3. 判断当前房屋在当前时间段内是否已经被预订
    4. 创建订单模型并设置相关数据
    5. 添加到数据库
    6. 返回响应
    :return:
    """

    # 1. 获取参数：房屋id，开始入住时间，结束入住时间
    data_dict = request.json
    house_id = data_dict.get("house_id")
    start_date_str = data_dict.get("start_date")
    end_date_str = data_dict.get("end_date")

    # 2. 判断参数/校验参数

    if not all([house_id, start_date_str, end_date_str]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 判断参数
    try:
        # 转成时间对象
        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")
        if start_date and end_date:
            assert start_date < end_date, Exception("结束日期必须大于开始时间")
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 判断房屋是否存在
    try:
        house = House.query.get(house_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据失败")

    if not house:
        return jsonify(errno=RET.NODATA, errmsg="未查询到房屋数据")

    # 3. 判断当前房屋在当前时间段内是否已经被预订
    try:
        conflict_orders = Order.query.filter(end_date > Order.begin_date, start_date < Order.end_date, Order.house_id == house_id).all()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据错误")

    if conflict_orders:
        return jsonify(errno=RET.DATAERR, errmsg="当前房屋已被预订")

    # 4. 创建订单模型并设置相关数据
    days = (end_date - start_date).days
    order = Order()
    order.user_id = g.user_id
    order.house_id = house_id
    order.begin_date = start_date
    order.end_date = end_date
    order.days = days
    order.house_price = house.price
    order.amount = days * house.price

    # 设置房屋的订单数量加1
    house.order_count += 1

    # 5. 添加到数据库
    try:
        db.session.add(order)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存订单失败")

    # 6. 返回响应
    return jsonify(errno=RET.OK, errmsg="OK")
