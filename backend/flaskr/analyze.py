from flask_restx import Namespace, Resource , fields ,reqparse  # RESTful API
from flaskr.extensions import redis_client      # 导入数据库
from flask_login import logout_user, login_required, current_user  # 用户认证
from function.analyze import read_data,get_recent,test_add_data,get_predict
from flask import request,jsonify

# 定义请求解析器

api = Namespace('analyze', description='数据分析接口')

@api.route('/analyze_dataget')
class analyze(Resource):
    @api.doc(description='数据分析')
    def post(self):
        '''
        数据分析
        '''     
        df = read_data()
        result = {}
        result['goods'],result['best_percate'],result['per_category_goods']= get_recent(df)
        return result
    
@api.route('/test_add_data')
class test_add_analyze(Resource):
    def post(self):
        '''
        测试-添加规律的销售记录
        '''     
        test_add_data()
        return 123

@api.route('/analyze_predict')
class analyze_predict(Resource):
    def post(self):
        '''
        测试-添加规律的销售记录
        '''     
        df = read_data()
        result = {}
        result['goods'] = get_predict(df)
        return result


@api.errorhandler
def handle_validation_error(error):
    return {'message': 'Validation failed', 'error': str(error)}, 410
