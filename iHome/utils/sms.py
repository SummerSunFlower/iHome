# coding=gbk

# coding=utf-8

# -*- coding: UTF-8 -*-

from iHome.libs.yuntongxun.CCPRestSDK import REST
import ConfigParser

# ���ʺ�
accountSid = '8aaf07085f5c54cf015f8c1710fa0f4d'

# ���ʺ�Token
accountToken = '711b641d76b34b06ab1a1fbc07fd381c'

# Ӧ��Id
appId = '8aaf07085f5c54cf015f8c1712620f54'

# �����ַ����ʽ���£�����Ҫдhttp://
serverIP = 'app.cloopen.com'

# ����˿�
serverPort = '8883'

# REST�汾��
softVersion = '2013-12-26'


class CCP(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            # ��ʼ��һ�����󣬲���ʹ�������ϵ����� `_instance` ���м�¼
            cls._instance = super(CCP, cls).__new__(cls, *args, **kwargs)
            # ����������������һ��rest����
            cls._instance.rest = REST(serverIP, serverPort, softVersion)
            # ����rest���������
            cls._instance.rest.setAccount(accountSid, accountToken)
            cls._instance.rest.setAppId(appId)
        return cls._instance

    def send_template_sms(self, to, datas, temp_id):
        """
        ����ģ�����
        :param to: ���յ��ֻ���
        :param datas: ����
        :param temp_id: ģ��id
        :return: ���Ϊ1�����ͳɹ������Ϊ0������ʧ��
        """
        result = self.rest.sendTemplateSMS(to, datas, temp_id)
        # ȡ�����ͽ��
        status_code = result.get("statusCode")

        if status_code == "000000":
            # ���ͳɹ�,����ֵΪ1�������ͳɹ�
            return 1
        else:
            # ����ʧ��
            return 0


if __name__ == '__main__':
    print CCP().send_template_sms("", ["888888", "5"], "1")


# ����ģ�����
# @param to �ֻ�����
# @param datas �������� ��ʽΪ���� ���磺{'12','34'}���粻���滻���� ''
# @param $tempId ģ��Id

# def sendTemplateSMS(to, datas, tempId):
#     # ��ʼ��REST SDK
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
