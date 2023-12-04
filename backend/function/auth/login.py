from function.sql import get_value
from werkzeug.security import check_password_hash
from flask_login import login_user
from flask import session,jsonify

from flaskr.models import User



user_data = {}
flag_init = True 
def data_init():
    '''
    页面数据初始化
    '''
    global user_data
    global flag_init 
    if flag_init:
        user_list = User.query.all()
        for user in user_list:
            user_id = user.user_id
            user_data[user_id]= {
                "user_name" : user.username,
                "user_rank" : user.rank,
                "user_power" : str(bin(user.power))[2:].zfill(4),
            }
        flag_init = False
def auth_login(data):
    '''通过输入的用户信息来进行用户登录\n
    input:\n
        request:前端返回的json数据\n
        request/user_name :邮箱\n
        request/password :密码\n
    output:\n
        data : josn文件\n
        data/code : 状态码\n
        data/msg : 具体信息(str)\n
        code : 状态码\n
    '''
    user_name = data["user_name"]
    password = data["password"]
    user = get_value(user_name, "username", "user")
    if not user:
        return {'message':"未找到该用户，请检测输入是否有误"},401
    if check_password_hash(user.password, password) or user.password== password:
        # 将用户id保存到cookie：
        session["username"] = user_name
        login_user(user)
        return {'message': '登录成功'}, 200
    else:
        return {'message': '密码错误'}, 402
def auth_show():
    '''
    展示当前所有的用户及其权限
    '''
    data_result = {}
    data_result["message"] = []
    data_init()
    for i in user_data:
        data_result["message"].append({
                "user_id":i,\
                "user_name" : user_data[i]["user_name"],\
                "user_rank" : user_data[i]["user_rank"],\
                "user_power" : user_data[i]["user_power"],\
                                       })
    return jsonify(data_result)
