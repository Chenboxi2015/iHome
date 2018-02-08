# coding:utf-8
# 调用短信接口

import logging
from CCPRestSDK import REST
import ConfigParser

accountSid = '8aaf07086150ec5001616a06e1a3077b'
# 说明：主账号，登陆云通讯网站后，可在控制台首页中看到开发者主账号ACCOUNT SID。

accountToken = 'f6afdbfa9c6d4d0ea97f7486596b166a'
# 说明：主账号Token，登陆云通讯网站后，可在控制台首页中看到开发者主账号AUTH TOKEN。

appId = '8aaf07086150ec5001616a06e20b0782'
# 请使用管理控制台中已创建应用的APPID。

serverIP = 'app.cloopen.com'
# 说明：请求地址，生产环境配置成app.cloopen.com。

serverPort = '8883'
# 说明：请求端口 ，生产环境为8883.

softVersion = '2013-12-26'  # 说明：REST API版本号保持不变。


#  同一个用户的请求初始化REST SDK的操作只需要执行一次,所以将调用短信接口的函数封装成类,--单例模式:只能有一个实例对象的类
# class CCP(object):
#     # 实现单例模式,只初始化一次
#     def __new__(cls):
#         if not hasattr(cls, '__instance'):
#             # 如果没有类属性,调用父类的new()方法生成实例对象赋值给类属性
#             cls.__instance = super.__new__(cls)
#
#             # 初始化REST SDK  # 为实例对象添加属性
#             cls.__instance.rest = REST(serverIP, serverPort, softVersion)
#             cls.__instance.rest.setAccount(accountSid, accountToken)
#             cls.__instance.rest.setAppId(appId)
#
#         return cls.__instance
#
#     # 发送模板短息方法
#     def send_template_sms(self, to, datas, temp_id):
#         # 尝试发送
#         try:
#             result = self.rest.sendTemplateSMS(to, datas, temp_id)
#         except Exception as e:
#             # 记录日志抛出异常
#             logging.error(e)
#             raise e
#         else:
#             return


# def sendTemplateSMS(to, datas, tempId):
#     # 初始化REST SDK
#     rest = REST(serverIP, serverPort, softVersion)
#     rest.setAccount(accountSid, accountToken)
#     rest.setAppId(appId)
#
#     result = rest.sendTemplateSMS(to, datas, tempId)
#     for k, v in result.iteritems():
#         if k == 'templateSMS':
#             for k, s in v.iteritems():
#                 print '%s:%s' % (k, s)
#         else:
#             print '%s:%s' % (k, v)
#
#
# if __name__ == '__main__':
#     sendTemplateSMS('18204681825', ['567899', '3'], 1)

class CCP(object):
    def __new__(cls):
        if not hasattr(cls, '__instance'):
            cls.__instance = super(CCP, cls).__new__(cls)
            # 初始化REST SDK
            cls.__instance.rest = REST(serverIP, serverPort, softVersion)
            cls.__instance.rest.setAccount(accountSid, accountToken)
            cls.__instance.rest.setAppId(appId)
        return cls.__instance

    # 发送短信函数
    def send_template_sms(self, to, datas, tempId):
        # 尝试发送短信
        try:
            result = self.__instance.rest.sendTemplateSMS(to, datas, tempId)
        except Exception as e:
            logging.error(e)
            # 抛出异常
            raise e
        return result.get('statusCode')
