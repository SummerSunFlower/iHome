# coding=gbk

# coding=utf-8

# -*- coding: UTF-8 -*-

from iHome.libs.yuntongxun.CCPRestSDK import REST
import ConfigParser

# 主帐号
accountSid = '8aaf07085f5c54cf015f8c1710fa0f4d'

# 主帐号Token
accountToken = '711b641d76b34b06ab1a1fbc07fd381c'

# 应用Id
appId = '8aaf07085f5c54cf015f8c1712620f54'

# 请求地址，格式如下，不需要写http://
serverIP = 'app.cloopen.com'

# 请求端口
serverPort = '8883'

# REST版本号
softVersion = '2013-12-26'


class CCP(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            # 初始化一个对象，并且使用类身上的属性 `_instance` 进行记录
            cls._instance = super(CCP, cls).__new__(cls, *args, **kwargs)
            # 比这个对象身上添加一个rest属性
            cls._instance.rest = REST(serverIP, serverPort, softVersion)
            # 设置rest的相关属性
            cls._instance.rest.setAccount(accountSid, accountToken)
            cls._instance.rest.setAppId(appId)
        return cls._instance

    def send_template_sms(self, to, datas, temp_id):
        """
        发送模板短信
        :param to: 接收的手机号
        :param datas: 数据
        :param temp_id: 模板id
        :return: 如果为1代表发送成功，如果为0代表发送失败
        """
        result = self.rest.sendTemplateSMS(to, datas, temp_id)
        # 取到发送结果
        status_code = result.get("statusCode")

        if status_code == "000000":
            # 发送成功,返回值为1，代表发送成功
            return 1
        else:
            # 发送失败
            return 0


if __name__ == '__main__':
    print CCP().send_template_sms("", ["888888", "5"], "1")


# 发送模板短信
# @param to 手机号码
# @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
# @param $tempId 模板Id

# def sendTemplateSMS(to, datas, tempId):
#     # 初始化REST SDK
#     rest = REST(serverIP, serverPort, softVersion)
#     rest.setAccount(accountSid, accountToken)
#     rest.setAppId(appId)
#
#     result = rest.sendTemplateSMS(to, datas, tempId)
#     for k, v in result.iteritems():
#
#         if k == 'templateSMS':
#             for k, s in v.iteritems():
#                 print '%s:%s' % (k, s)
#         else:
#             print '%s:%s' % (k, v)


# sendTemplateSMS("18513174598", ["666666", "5"], "1")
# sendTemplateSMS("18513174598", ["666666", "5"], "1")
# sendTemplateSMS("18513174598", ["666666", "5"], "1")
# sendTemplateSMS("18513174598", ["666666", "5"], "1")
