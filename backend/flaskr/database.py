from flask_restx import Namespace, Resource    # RESTful API
from flaskr.extensions import db      # 导入数据库
import flaskr.models  # 务必导入模型
from flaskr import redis_client

api = Namespace('database', description='数据库操作接口')


@api.route('/create')
class Create(Resource):
    @api.doc(description='创建数据库,只用执行一次。重复执行视为测试数据库连接')
    def get(self):
        '''
        创建数据库
        '''
        try:
            db.create_all()
            return {'message': '创建成功'}, 200
        except:
            return {'message': '创建失败'}, 500



@api.route('/drop')
class Drop(Resource):
    @api.doc(description='删除数据库')
    def get(self):
        """
        删除数据库
        """
        try:
            db.drop_all()
            if redis_client.exists('goods_num') : redis_client.delete('goods_num')
            if redis_client.exists('User') : redis_client.delete('goods_num')   
            return {'message': '删库成功'}, 200
        except:
            return {'message': '删库成功'}, 200
