# -*- coding:utf-8 -*-
# 验证码的提供：图片验证码和短信验证码
import re, random
from flask import abort
from flask import current_app
from flask import json
from flask import make_response
from flask import request, jsonify

from iHome import constants
from iHome.utils.captcha.captcha import captcha

from iHome.utils.responce_code import RET
from . import api
from iHome import redisstorge


@api.route("/sms_code", methods=["POST"])
def send_sms_code():
    """
    发送短信验证码
    1. 接收前端发送过来的参数：手机号，用户输入图片验证码的内容，图片验证码的编号
    2. 判断参数是否都有值与参数校验
    3. 从redis中取出正确的图片验证码(如果没有到，代表验证码过期)
    4. 进行验证码的对比，如果用户输入的验证码与真实的验证码一样
    5. 生成短信验证码
    6. 发送短信
    7. 保存短信验证到redis中
    8. 告诉前端发送短信成功
    :return:
    """
    # 1. 接收前端发送过来的参数
    # JSON字符串
    print("test1")
    json_data = request.data
    # 转成字典
    json_dict = json.loads(json_data)

    mobile = json_dict.get("mobile")
    image_code = json_dict.get("image_code")
    image_code_id = json_dict.get("image_code_id")

    # 2. 判断参数是否有值和参数校验
    if not all([mobile, image_code, image_code_id]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    if not re.match("^1[34578][0-9]{9}$", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="手机号格式有误")

    # 3. 从redis中取出正确的图片验证码(如果没有到，代表验证码过期)
    try:
        real_image_code = redisstorge.get("ImageCode:" + image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询验证码出错")

    # 如果没有到，代表验证码过期
    if not real_image_code:
        return jsonify(errno=RET.NODATA, errmsg="验证码已过期")

    # 4. 进行验证码的对比，如果用户输入的验证码与真实的验证码一样
    if image_code.lower() != real_image_code.lower():
        return jsonify(errno=RET.DATAERR, errmsg="验证码输入不正确")

    # 5. 生成短信验证码
    sms_code = "%06d" % random.randint(0, 999999)
    current_app.logger.debug("短信验证码为：" + sms_code)
    # 6. 发送短信
    # result = CCP().send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES / 60], "1")
    # if result != 1:
    #     # 发送短信失败
    #     return jsonify(errno=RET.THIRDERR, errmsg="发送短信失败")

    # 7. 保存短信验证到redis中
    try:
        redisstorge.set("Mobile:" + mobile, sms_code, constants.SMS_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存验证码失败")
    # 8. 告诉前端发送短信成功
    return jsonify(errno=RET.OK, errmsg="发送成功")



@api.route("/image_code")
def get_image_code():
    """
    图片验证码的视图函数
    1. 取到图片编码
    2. 生成图片验证码
    3. 将图片验证码内容通过图片编码保存到redis中
    4. 返回图片

    :return:
    """
    # 1. 取到图片编码
    cur_id = request.args.get("cur_id")
    pre_id = request.args.get("pre_id")

    if not cur_id:
        abort(403)

    # 2. 生成图片验证码
    _, text, image = captcha.generate_captcha()
    current_app.logger.debug("图片验证码为：" + text)
    # 3. 将图片验证码内容通过图片编码保存到redis中
    try:
        redisstorge.set("ImageCode:" + cur_id, text, constants.IMAGE_CODE_REDIS_EXPIRES)
        if pre_id:
            redisstorge.delete("ImageCode:" + pre_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存验证码数据失败")

    # 返回图片验证码的图片
    response = make_response(image)
    # 设置响应的内容类型
    response.headers["Content-Type"] = "image/jpg"
    # 进行返回
    return response
