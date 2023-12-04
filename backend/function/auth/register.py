from function.sql import get_value,upload_data
from werkzeug.security import generate_password_hash
from flask_login import login_user
import re

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
