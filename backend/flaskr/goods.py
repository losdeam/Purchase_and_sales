from flask_restx import Namespace, Resource , fields   # RESTful API
from flaskr.extensions import db ,redis_client      # 导入数据库
from function.goods import good_add,good_sell,good_nums_verify,good_Replenish,good_show
import flaskr.models  # 务必导入模型
import datetime 
api = Namespace('goods', description='商品操作接口')

add_model = api.model('addmodel', {
    'good_name': fields.String(max_length=100, required=True, description='商品名称'),
    'good_num': fields.Integer(required=True, description='商品库存数量'),
    'good_price_buying': fields.Float(required=True, description='商品进货价格'),
    'good_price_retail': fields.Float(required=True, description='商品零售价格'),
    'good_sort': fields.String(max_length=100, required=True, description='商品分类'),
    'good_baseline': fields.Integer(required=True, description='商品最低库存量'),
})

change_model = api.model('changemodel',{
    'good_id': fields.Integer(required=True, description='商品id'),
    'change_num': fields.Integer(required=True, description='商品售出/进货数量'),
})

@api.route('/add')
class add(Resource):
    @api.doc(description='全新商品购入')
    @api.expect(add_model, validate=True)
    def post(self):
        '''
        全新商品购入
        '''
        good_name = api.payload['good_name']
        good_num = api.payload['good_num']
        good_price_buying = api.payload['good_price_buying']
        good_price_retail = api.payload['good_price_retail']
        good_sort = api.payload['good_sort']
        good_baseline = api.payload['good_baseline']
        return  good_add(good_name ,good_num,good_price_buying,good_price_retail,good_sort,good_baseline)

@api.route('/Replenish')
class Replenish(Resource):
    @api.doc(description='商品补货')
    @api.expect(change_model, validate=True)
    def post(self):
        """
        商品数量增加
        """
        id = api.payload['good_id']
        nums = api.payload['change_num']
        return good_Replenish(id,nums)

@api.route('/sell')
class sell(Resource):
    @api.doc(description='商品卖出')
    @api.expect(change_model, validate=True)
    def post(self):
        """
        商品数量减少
        """
        id = api.payload['good_id']
        nums = api.payload['change_num']
        return good_sell(id,nums)

@api.route('/show')
class show(Resource):
    @api.doc(description='展示商品')
    def post(self):
        '''
        '''
        return good_show()
