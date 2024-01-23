from flask_restx import Namespace, Resource    # RESTful API
from flaskr.extensions import mongo,redis_client   # 导入数据库

from flaskr import redis_client
from function.util import yaml_read,data_to_mongo,hash_password,data_init
import os 
api = Namespace('database', description='数据库操作接口')


@api.route('/create')
class Create(Resource):
    @api.doc(description='创建数据库,只用执行一次。重复执行视为测试数据库连接')
    def get(self):
        '''
        创建数据库
        '''
        try:
            # print(os.getcwd())
            data = {
                "id" : 0,
                "name" : "adm",
                "password" : hash_password("111"),
                "rank" : 1,
                "power" : 15,
                # "path_config" : yaml_read('./instance/path_config.yaml'),
                # "data_config" : yaml_read('./instance/data_config.yaml'),
                # "train_config" : yaml_read('./instance/train_config.yaml'),
            }
            # print(data)s
            message,flag = data_to_mongo('user_data',data)
            if not flag :
                return {'message': '创建失败'}, 500
            data_init()
            return {'message': '创建成功'}, 200
        except Exception as e :
            print(e)
            return {'message': '创建失败'}, 500
@api.route('/drop')
class Drop(Resource):
    @api.doc(description='删除数据库')
    def get(self):
        """
        删除数据库
        """
        try:
            # 获取数据库中的所有集合名称
            collection_names = mongo.db.list_collection_names()

            # 删除每个集合
            for collection_name in collection_names:
                mongo.db.drop_collection(collection_name)

            return {'message': '删库成功'}, 200
        except:
            return {'message': '删库成功'}, 200
