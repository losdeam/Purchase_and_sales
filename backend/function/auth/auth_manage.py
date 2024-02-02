# from function.sql import upload_data,get_value, get_values,get_values_time,delete_value,update_data
# from flaskr.models import Goods
# from flaskr.models import User
from flaskr.extensions import redis_client,login_manager
from flask_login import login_user,UserMixin,current_user
from flask import jsonify
from function.util import hash_password,verify_password,get_data,data_get_mongo,load_data,data_verify_total,yaml_read
from function.util import data_to_mongo ,data_from_mongo,data_update_mongo,data_delete_mongo
import re
import json

class User(UserMixin):
    def __init__(self, user_data ):
        self.id = user_data['id']
        self.power =user_data['power']
        self.name = user_data['name']
        self.rank = user_data['rank']
    def get_id(self):
        return str(self.id)
    
# 用户加载函数
@login_manager.user_loader
def load_user(user_id):
    user_data = data_from_mongo('user_data',{'id':int(user_id)})[0]
    # print(12312131311,user_data)
    if user_data:
        return User(user_data)
    return None
 
def auth_show():
    '''
    展示当前所有的用户及其权限
    '''
    data_result = {}
    data_result["message"] = []
    user_name_list = redis_client.hkeys('user_data')
 
    for user_name in user_name_list:

        user_data = get_data('user_data',user_name)

        data_result["message"].append({
                "user_id":user_data["id"],\
                "user_name" : user_data["name"],\
                "user_rank" : user_data["rank"],\
                "user_power" : user_data["power"],\
                                       })
    return data_result
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
def delete_auth(name):
    '''
    在拥有管理员身份的前提下，对用户进行删除\n
    '''
    result = {}
    data_delete_mongo(name,"name","user_data")
    redis_client.hdel("user_data", name)
    result["message"] = f"用户{name},已成功删除"
    return jsonify(result) 

def auth_update(user_id,new_data):
    data_result = {}
    data_result["message"] = data_update_mongo(user_id,"id","user_data",new_data)
    result = jsonify(data_result)
    return result
def auth_register(data):
    '''用户注册\n
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
    # -------------------密码安全性验证-------------
    password = data["password"]
    flag, msg = check_password_secure(password)
    if flag != 200:
        data_result["message"] = msg
        return data_result, 403
    # --------------------------------
    data = {
        "name" : data["name"],
        "password" :hash_password(data["password"]) ,
        "rank" : data['rank'],
        "power" : data['power'],
        "path_config" : yaml_read('./instance/path_config.yaml'),
        "data_config" : yaml_read('./instance/data_config.yaml'),
        "train_config" : yaml_read('./instance/train_config.yaml'),
    }

    message,flag = data_to_mongo('user_data',data)

    # print(12312321,message,flag)
    if not flag :
        return {'message': message}, 500
    return {'message': '创建成功'}, 200
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

    user = get_data('user_data',user_name)
    # print(user)
    if not user:
        return {'message':"未找到该用户，请检测输入是否有误"},401
    if verify_password(data_get_mongo('user_data','password',{"name":user_name}), password):
        user = User(user)
        # print(current_user)
        login_user(user, remember=True)
        # print(current_user)
        # 将用户id保存到cookie：

        return {'message': '登录成功'}, 200
    else:
        return {'message': '密码错误'}, 402
def auth_get_config():
    redis_client

