from flask_restx import Namespace, Resource, fields
# from function.auth import get_email_captcha, test_captcha, login_man, regist
from flask_login import logout_user, login_required, current_user  # 用户认证
from flaskr.extensions import db, login_manager
from flaskr.models import User


api = Namespace('auth', description='用户认证相关接口')


@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(db.select(User).where(User.user_id == user_id)).scalar_one_or_none()


email_model = api.model('EmailModel', {
    'email': fields.String(max_length=100, required=True, description='邮箱'),
})

user_mian_model = api.clone('UserMainModel', email_model, {
    'password': fields.String(max_length=128, required=True, description='密码'),
})

user_model = api.clone('UserModel', user_mian_model, {
    'username': fields.String(max_length=50, required=True, description='用户名'),
})

user_captcha_model = api.clone('UserCaptchaModel', user_model, {
    'captcha': fields.String(max_length=4, required=True, description='验证码')
})



@api.route('/login')
class Login(Resource):
    @api.expect(user_mian_model, validate=True)
    @api.doc(description='登录，\
            输入  email :邮箱，password :密码')
    def post(self):
        '''
        登录接口
        '''
        if current_user.is_authenticated:  # type: ignore
            return {'message': '用户已登录'}, 403

        args = api.payload

        return login_man(args)


@api.route('/logout')
class Logout(Resource):
    @api.doc(description='登出')
    @login_required  # 权限控制，必须先登录
    def get(self):
        '''
        登出接口
        '''
        logout_user()
        return {'message': '登出成功'}, 200
