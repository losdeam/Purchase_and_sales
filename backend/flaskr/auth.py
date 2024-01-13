from flask_restx import Namespace, Resource, fields
from function.auth import auth_login,auth_register,auth_show,delete_auth,User
from flask_login import logout_user, login_required, current_user,UserMixin # 用户认证
from flaskr.extensions import db, login_manager
from function.util import data_find_mongo,data_get_mongo
from flask import session
import secrets







api = Namespace('auth', description='用户认证相关接口')



userModel = api.model('userModel', {
    'user_name': fields.String(max_length=100, required=True, description='用户名'),
    'password' :fields.String(max_length=100, required=True, description='密码'),
})
registerModel = api.model('registerModel', {
    'name': fields.String(max_length=100, required=True, description='用户名'),
    'password' :fields.String(max_length=100, required=True, description='密码'),
    'rank' :fields.Integer(required=True, description='用户权限设置'),
    'power' :fields.Integer(required=True, description='用户能力设置，'),
})
deleteModel = api.model('registerModel', {
    'user_id': fields.String(max_length=100, required=True, description='用户id'),})
@api.route('/register')
class Register(Resource):
    # @login_required  # 权限控制，必须先登录
    @api.doc(description='注册，\
             输入  user_name :用户名，password :密码,rank :用户权限设置,power :用户能力设置，')
    @api.expect(registerModel, validate=True)
    def post(self):
        '''
        注册接口
        '''
        # print(1)
        # print(current_user)
        # print(current_user.__dir__())
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
            logout_user()
        args = api.payload
        # print(args)
        data = auth_login(args)
        return data
@api.route('/logout')
class Logout(Resource):
    @api.doc(description='登出')
    @login_required  # 权限控制，必须先登录
    def post(self):
        '''
        登出接口
        '''
        logout_user()
        return {'message': '登出成功'}, 200
@api.route('/show')
class show(Resource):
    @api.doc(description='显示')
    # @login_required  # 权限控制，必须先登录
    def post(self):
        '''
        显示已有用户
        '''
        return auth_show()
@api.route('/delete')
class delete(Resource):
    @login_required  # 权限控制，必须先登录
    # @api.expect(deleteModel, validate=True)
    @api.doc(description='删除用户')
    def post(self):
        '''
        删除用户
        '''
        if (current_user.power >>3) &1 :  # type: ignore
            name = api.payload['user_name']
            return delete_auth(name)
        return {'message': '当前用户不具有删除其他用户的权限'}, 403     
@api.route('/update')
class update(Resource):
    @api.doc(description='商品数据更改')
    def post(self):
        '''
        对商品数据进行修改
        '''
        if (current_user.power >>1) &1 :  # type: ignore
            user_id = api.payload['user_id']
            new_data = api.payload['new_data']
        
            return  delete_auth(user_id ,new_data)
        return {'message': '当前用户不具有修改商品信息的权限'}, 403     
