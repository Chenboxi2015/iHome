# -*- coding:utf8 -*-
from . import api
from flask import jsonify,make_response
from ihome.utils.captcha.captcha import captcha
from ihome import redis_store
from ihome.utils import constants
import logging
from ihome.utils.response_code import RET


# /api/v1_0/image_codes/image_code_id
@api.route('/image_codes/<image_code_id>')
def get_image_codes(image_code_id):
    # 前端传递uuid -->服务器生成验证码(文本和图片)--> 存储到redis中:image_code_id:text--> 返回图片数据
    # 生成图像验证码
    name, text, image_data = captcha.generate_captcha()
    # 存储到Redis中  设置过期时间180s setex
    # 参数 key expiretime value
    #     image_code_image_code_id 180 text
    try:
        redis_store.setex('image_code_%s' % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRE, text)
    except Exception as e:
        # 记录错误日志
        logging.error(e)
        resp_dict = {
            'errcode': RET.DBERR,
            'errmsg': '设置redis错误'
        }
        return jsonify(resp_dict)

    # 返回图片
    resp = make_response(image_data)
    resp.headers['Content-Type'] = 'image/jpg'
    return resp
