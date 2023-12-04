from function.sql import get_value
from werkzeug.security import check_password_hash
from flask_login import login_user


def login_man(data):
    '''通过输入的用户信息来进行用户登录\n
    input:\n
        request:前端返回的json数据\n
        request/email :邮箱\n
        request/password :密码\n
    output:\n
        data : josn文件\n
        data/code : 状态码\n
        data/msg : 具体信息(str)\n
        code : 状态码\n
    '''
    email = data["email"]
    password = data["password"]
    user = get_value(email, "email", "user")
    if not user:
        return "未找到邮箱，请检测输入是否有误"
    if check_password_hash(user.password, password):
        # 将用户id保存到cookie：
        login_user(user)
        return {'message': '登录成功'}, 200
    else:
        return {'message': '密码错误'}, 401
