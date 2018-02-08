# -*- coding:utf8 -*-
from . import api
from flask import jsonify, make_response, request
from ihome.utils.captcha.captcha import captcha
from ihome import redis_store
from ihome.utils import constants
import logging
from ihome.utils.response_code import RET
import random
from ihome.models import User
from ihome.libs.yuntongxin.sms import CCP


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


# 短信验证码
# /api/v1_0/sms_codes/?mobile=18204681825&code=45DR&codeId=738e44-e814-4225-9993-96fa8feaf9fb
@api.route('/sms_codes/<re(r"1[345678]\d{9}"):mobile>')
def get_sms_codes(mobile):
    # 获取参数
    code = request.args.get('code')
    codeId = request.args.get('codeId')

    # 参数校验
    if not all([code, codeId]):
        resp = {
            'errcode': RET.DATAERR,
            'errmsg': '数据不完整'
        }
        return jsonify(resp)
    # 业务处理

    # 2 获取图片验证码
    image_code_id = 'image_code_' + codeId
    try:
        new_code = redis_store.get(image_code_id)
    except Exception as e:
        logging.error(e)
        resp = {
            'errcode': RET.DBERR,
            'errmsg': '获取图片验证码失败'
        }
        return jsonify(resp)
    # 图片验证码是否有效
    if new_code is None:
        resp_dict = {
            'errno': RET.NODATA,
            'errmsg': '图片验证码过期/失效'
        }
        return jsonify(resp_dict)

    # 删除原来的验证码
    try:
        redis_store.delete(image_code_id)
    except Exception as e:
        logging.error(e)
        resp = {
            'errcode': RET.DBERR,
            'errmsg': '删除图片验证码失败'
        }
        return jsonify(resp)

    # 3 对比是否一致
    if new_code.lower() != code.lower():
        # 不一致
        resp = {
            'errcode': RET.PARAMERR,
            'errmsg': '图片二维码填写错误'
        }
        return jsonify(resp)

    # 1 用户名是否存在
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        logging.error(e)
        resp = {
            'errcode': RET.DBERR,
            'errmsg': '查找用户信息失败'
        }
        return jsonify(resp)
    if user:
        # 用户存在
        resp = {
            'errcode': RET.DATAEXIST,
            'errmsg': '该用户已存在'
        }
        return jsonify(resp)
    # 创建6位验证码
    sms_code = '%06d' % random.randint(0, 999999)
    # 将短信验证码存储到Redis中  点击注册时进行对比
    try:
        redis_store.setex('sms_code_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRE, sms_code)
    except Exception as e:
        logging.error(e)
        resp = {
            'errcode': RET.DBERR,
            'errmsg': '保存短信验证码失败'
        }
        return jsonify(resp)
    # 发送验证码
    ccp = CCP()
    status_code = ccp.send_template_sms('18204681825', [sms_code, constants.SMS_CODE_TIME_EXPIRE], 1)
    # 返回数据
    if status_code == '000000':
        resp = {
            'errcode': RET.OK,
            'errmsg': '发送短信验证码成功'
        }
        return jsonify(resp)
    else:
        resp = {
            'errcode': RET.THIRDERR,
            'errmsg': '发送短信验证码失败'
        }
        return jsonify(resp)



