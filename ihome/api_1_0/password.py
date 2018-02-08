# -*- coding:utf8 -*-
# 实现登录 注册和退出登录
from . import api
from flask import request, jsonify, session
from ihome.utils.response_code import RET
import re, logging
from ihome import redis_store, db
from ihome.models import User
from ihome.utils import constants


# /api/v1_0/users 注册 post
# 参数 mobile sms_code password
@api.route('/users', methods=['POST'])
def register():
    # 获取参数
    resp_json = request.get_json()
    mobile = resp_json.get('mobile')
    sms_code = resp_json.get('sms_code')
    password = resp_json.get('password')
    # 参数校验
    # 1 数据完整性
    if not all([mobile, sms_code, password]):
        return jsonify(errno=RET.PARAMERR, errmsg='数据不完整')
    # 2 手机号格式
    if not re.match(r"1[345678]\d{9}", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg='手机号格式不正确')

    # 业务处理
    # Redis中取出短信验证码
    try:
        real_sms_code = redis_store.get('sms_code_' + mobile)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='获取Redis数据错误')
    # 短信验证码是否失效
    if not real_sms_code:
        return jsonify(errno=RET.DATAERR, errmsg='短信验证码过期或不存在')
    # 对比短信验证码是否一致
    if real_sms_code != sms_code:
        return jsonify(errno=RET.PARAMERR, errmsg='短信验证码输入错误，请重新输入')
    # 删除短信Redis--》可以修改后重新输入
    try:
        redis_store.delete('sms_code_' + mobile)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='删除Redis数据错误')
    # 查询用户是否存在
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='用户表查询失败')
    if user:
        return jsonify(errno=RET.DATAEXIST, errmsg='该用户已注册，请去登录')
    # 将用户信息保存到数据库中
    user = User(name=mobile, mobile=mobile)
    # 密码需要加密
    user.password = password
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg='添加用户失败')
    # 保存用户登录状态并跳转到登录页
    try:
        session['id'] = user.id
        session['name'] = user.mobile
        session['mobile'] = user.mobile
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='session存储错误')

    # 返回数据
    return jsonify(errno=RET.OK, errmsg='用户注册成功')


# /api/v1_0/sessions 登录 post
# 参数 mobile password
@api.route('/sessions', methods=['POST'])
def login():
    # 获取参数
    resp_json = request.get_json()
    mobile = resp_json.get('mobile')
    password = resp_json.get('password')
    # 参数校验
    # 1 数据完整性
    if not all([mobile, password]):
        return jsonify(errno=RET.PARAMERR, errmsg='数据不完整')
    # 2 手机号格式
    if not re.match(r"1[345678]\d{9}", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg='手机号格式不正确')
    # 业务处理
    # 用户ip
    user_ip = request.remote_addr
    try:
        real_count = redis_store.get('access_' + user_ip)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询Redis失败')
    # Redis存储错误次数 不大于5次
    if real_count and int(real_count) >= constants.LOGIN_ERROR_MAX_NUM:
        return jsonify(errno=RET.REQERR, errmsg='请求已超过最大次数')
    # 用户名是否存在
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='用户查询失败')
    # 用户是否存在或者密码是否正确
    if user is None or not user.check_password(password):
        # 错误一次加一 设置过期时间
        try:
            redis_store.incr('access_' + user_ip)
            redis_store.expire('access_' + user_ip, constants.LOGIN_ERROR_FORBID_TIME)
        except Exception as e:
            logging.error(e)
            return jsonify(errno=RET.DBERR, errmsg='Redis操作失败')
        return jsonify(errno=RET.LOGINERR, errmsg='用户名或密码输入错误')
    # 如果输入正确 错误次数清零
    try:
        redis_store.delete('access_' + user_ip)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='删除Redis数据失败')
    # 保存登录状态
    try:
        session['id'] = user.id
        session['name'] = user.mobile
        session['mobile'] = user.mobile
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='用户登录失败')
    # 返回数据
    return jsonify(errno=RET.OK, errmsg='用户登录成功')
