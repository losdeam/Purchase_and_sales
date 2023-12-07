from function.sql import upload_data,get_value, get_values,get_values_time,delete_value,update_data
from flaskr.models import Goods
from flaskr.models import User
from flask_login import login_user
from flask import jsonify
from werkzeug.security import generate_password_hash,check_password_hash
import re


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
def change_auth_data():
    '''
    在拥有管理员身份的前提下，对用户权限进行修改\n
        input :\n
        user_id:用户id\n
        new_user_name :用户名\n
        new_user_password:密码\n
        rank : 二进制，以位运算的方式确认权限\n
    需进行操作：\n
    1. 用户名设置\n
    2. 密码设置 \n
    3. 权限赋予\n
    '''
    pass
def delete_auth(user_id):
    '''
    在拥有管理员身份的前提下，对用户进行删除\n
    '''
    result = {}
    data_init()
    delete_value(user_id,"user_id","user")
    del user_data[user_id]
    result["message"] = f"用户{user_id},已成功删除"
    return jsonify(result) 
def auth_register(data):
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
    data_result = {}
    data_result["message"] = ""
    user_name = data["user_name"]
    password = data["password"]
    rank = data['rank']
    power = data['power']
    user = get_value(user_name, "username", "user")
    if  user:
        data_result["message"] = "已存在同名用户"
        return data_result , 401 
    flag, msg = check_password_secure(password)
    password =generate_password_hash(password)
    if flag != 200:
        data_result["message"] = msg
        return data_result, 403
    upload_data({"username": user_name, "password": password,
                 "rank": rank,"power": power}, "user")
    data = get_value(user_name,"username","user")
    user_data[data.user_id]= {
                "user_name" : user_name,
                "user_rank" : rank,
                "user_power" : str(bin(power))[2:].zfill(4),
            }
    data_result["message"] = "注册成功"

    return data_result, 200
def check_password_secure(password):
    '''
    密码安全性判断
    return： flag: 是否可行
            msg : 不可行的话给出原因，可行返回密码安全性
    '''
    '''密码安全性判断\n
    input:\n
        password:密码\n
    output:\n
        code : 状态码\n
        msg : 具体信息\n
    '''
    # 初始化分数
    score = 0
    # 长度判定
    length = len(password)
    if length < 8:
        return 403, "密码长度至少需要8位"
    else:
        score += length
    # 字符类型判定
    has_upper = re.search(r'[A-Z]', password)
    has_lower = re.search(r'[a-z]', password)
    has_digits = re.search(r'[0-9]', password)
    has_symbol = re.search(r'[ !#$%&\'()*+,-./[\\\]^_`{|}~"+:=?]', password)
    char_types = [1 if i else 0 for i in (
        has_upper, has_lower, has_digits, has_symbol)]
    if sum(char_types) < 2:
        return 403, "密码需要包含多种字符类型"
    else:
        score += 10 * sum(char_types)
    # 常见密码或日期判定
    if password.lower() in ['password', '123456'] or re.match(r'\d{4,}', password):
        return 403, "密码不能是常见密码或连续数字"
    if score >= 45:
        return 200, "非常安全的密码"
    elif score >= 30:
        return 200, "安全性一般的密码"
    return 403, "密码安全性过低"
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
        login_user(user, remember=True)
        # 将用户id保存到cookie：
        return {'message': '登录成功'}, 200
    else:
        return {'message': '密码错误'}, 402
