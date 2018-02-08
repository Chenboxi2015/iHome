# -*- coding:utf8 -*-

# 图片验证码过期时间
IMAGE_CODE_REDIS_EXPIRE = 180
# 短信验证码过期时间
SMS_CODE_REDIS_EXPIRE = 300
# 短信验证码的过期分钟
SMS_CODE_TIME_EXPIRE = 5
# 登录的最大错误次数
LOGIN_ERROR_MAX_NUM = 5
# 登录错误封ip的时间，单位：秒
LOGIN_ERROR_FORBID_TIME = 3600