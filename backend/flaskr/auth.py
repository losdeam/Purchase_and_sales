from flask_restx import Namespace, Resource, fields
from function.auth import auth_login,auth_register,auth_show
from flask_login import logout_user, login_required, current_user  # 用户认证
from flaskr.extensions import db, login_manager
from flaskr.models import User


api = Namespace('auth', description='用户认证相关接口')


@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(db.select(User).where(User.user_id == user_id)).scalar_one_or_none()


userModel = api.model('userModel', {
    'user_name': fields.String(max_length=100, required=True, description='用户名'),
    'password' :fields.String(max_length=100, required=True, description='密码'),
})
registerModel = api.model('registerModel', {
    'user_name': fields.String(max_length=100, required=True, description='用户名'),
    'password' :fields.String(max_length=100, required=True, description='密码'),
    'rank' :fields.Integer(required=True, description='用户权限设置'),
    'power' :fields.Integer(required=True, description='用户能力设置，'),
})
@api.route('/register')
class Register(Resource):
    @api.doc(description='注册，\
             输入  user_name :用户名，password :密码,rank :用户权限设置,power :用户能力设置，')
    @api.expect(registerModel, validate=True)
    @login_required  # 权限控制，必须先登录
    def post(self):
        '''
        注册接口
        '''
        if (current_user.power >>3) &1 :  # type: ignore
            args = api.payload
            return auth_register(args)
        return {'message': '当前用户不具有创建新用户的权限'}, 403
        



@api.route('/login')
class Login(Resource):
    @api.expect(userModel, validate=True)
    @api.doc(description='登录，\
            输入  email :邮箱，password :密码')
    
    def post(self):
        '''
        登录接口
        '''
        if current_user.is_authenticated:  # type: ignore
            return {'message': '用户已登录'}, 403

        args = api.payload

        return auth_login(args)


@api.route('/logout')
class Logout(Resource):
    @api.doc(description='登出')
    @login_required  # 权限控制，必须先登录
    def get(self):
        '''
        登出接口
        '''
        print("111")
        logout_user()
        return {'message': '登出成功'}, 200

@api.route('/show')
class show(Resource):
    @api.doc(description='显示')
    def post(self):
        '''
        显示已有用户
        '''
        return auth_show()