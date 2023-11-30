from flask_mail import Message
import string
import random
import re
import threading
from time import sleep
from werkzeug.security import generate_password_hash
from flaskr.extensions import mail
from function.sql import get_value, upload_data

event = None
times = 300  # 验证码保留秒数

email_dict = {"test": "1234"}
# 获取并发送验证码，并临时建立邮箱与验证码的映射

def get_email_captcha(email):
    '''通过输入的邮箱来发送验证码\n
    input:\n
        email:用户输入的邮箱\n
    output:\n
        None
    '''
    global email_dict
    # 4/6：随机数组、字母、数组和字母的组合
    source = (string.digits+string.ascii_uppercase)*4
    captcha = random.sample(source, 4)
    captcha = "".join(captcha)
    data = {}

    message = Message(subject="注册验证码", recipients=[
                      email], body=f"您的验证码是:{captcha},仅在五分钟内有效")
    try:
        mail.send(message)
    except:
        data["code"] = 404
        data["msg"] = "验证码发送失败，请检查邮箱是否存在"
        return data, data["code"]
    email_dict[email] = captcha
    data["code"] = 200
    data["msg"] = "验证码发送成功"

    global event
    if event:
        event.set()  # 终止旧线程

    event = threading.Event()
    new_thread = threading.Thread(target=captcha_sleep, args=(email, event))
    new_thread.start()

    return data, data["code"]


def captcha_sleep(email, event):
    '''在休眠一定时间后在全局变量email_dict中删除\n
    input:\n
        email:用户输入的邮箱\n
    output:\n
        None
    '''
    sleep(times)  # 模拟sleep
    if event.is_set():
        return
    if email in email_dict:
        del email_dict[email]

def regist(request):
    '''通过输入的用户信息来进行用户注册\n
    input:\n
        request:前端返回的json数据\n
        request/name :用户名\n
        request/password :密码\n
        request/email :邮箱\n
        request/captcha :验证码\n
    output:\n
        data : josn文件\n
        data/code : 状态码\n
        data/msg : 具体信息(str)\n
        code : 状态码\n
    '''

    name = request["username"]
    password = request["password"]
    email = request["email"]
    captcha = request["captcha"]

    data = {}
    if get_value(name, "username", "user"):
        data["code"] = 400
        data["msg"] = "用户名已存在"
        return data, data["code"]
    if get_value(email, "email", "user"):
        data["code"] = 401
        data["msg"] = "该邮箱已被注册"
        return data, data["code"]
    if email not in email_dict:
        data["code"] = 402
        data["msg"] = "请先获取验证码"
        return data, data["code"]
    if email_dict[email] != captcha:
        data["code"] = 403
        data["msg"] = "验证码错误"
        return data, data["code"]

    flag, msg = check_password_secure(password)
    password = generate_password_hash(password)

    if flag != 200:
        data["code"] = flag
        data["msg"] = msg
        return data, 403
    upload_data({"username": name, "password": password,
                 "email": email}, "user")
    data["code"] = 200
    data["msg"] = "注册成功"
    return data, 200


def test_captcha():
    return email_dict


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
