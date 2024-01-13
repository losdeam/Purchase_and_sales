from flask_restx import Namespace, Resource , fields ,reqparse  # RESTful API
from flaskr.extensions import db ,redis_client      # 导入数据库
from flask_login import logout_user, login_required, current_user  # 用户认证
from function.goods import goods_add,goods_sell,goods_nums_verify,goods_Replenish,goods_show,show_sale_record,goods_delete,goods_conifg,goods_delete_f
from function.recognition import train_new_label
from flask import request,jsonify

# 定义请求解析器

api = Namespace('goods', description='商品操作接口')
add_model = api.model('addmodel', {
    'goods_name': fields.String(max_length=100, required=True, description='商品名称'),
    'goods_num': fields.Integer(required=True, description='商品库存数量'),
    'goods_price_buying': fields.Float(required=True, description='商品进货价格'),
    'goods_price_retail': fields.Float(required=True, description='商品零售价格'),
    'goods_sort': fields.String(max_length=100, required=True, description='商品分类'),
    'goods_baseline': fields.Integer(required=True, description='商品最低库存量'),
})
change_model = api.model('changemodel',{
    'goods_id': fields.Integer(required=True, description='商品id'),
    'change_num': fields.Integer(required=True, description='商品售出/进货数量'),
    'type': fields.Integer(required=True, description='商品售出/进货类型')

})
delete_model = api.model('deletemodel',{
    'goods_id': fields.Integer(required=True, description='商品id'),
})

@api.route('/add')
class add(Resource):
    # @login_required  # 权限控制，必须先登录
    @api.doc(description='全新商品购入')
    @api.expect(add_model, validate=True)
    def post(self):
        '''
        全新商品购入
        '''
        if (current_user.power >>2) &1 :  # type: ignore
            goods_name = api.payload['goods_name']
            goods_num = api.payload['goods_num']
            goods_price_buying = api.payload['goods_price_buying']
            goods_price_retail = api.payload['goods_price_retail']
            goods_sort = api.payload['goods_sort']
            goods_baseline = api.payload['goods_baseline']
            data_sql = goods_add(goods_name ,goods_num,goods_price_buying,goods_price_retail,goods_sort,goods_baseline)
            result = jsonify(data_sql)
            result.status_code = data_sql['code']
            return result

        result = jsonify({'message': '当前用户不具有添加新商品的权限'})
        result.status_code = 406  
        return result 
   
@api.route('/change')
class Replenish(Resource):
    @api.doc(description='商品数量改变')
    @api.expect(change_model, validate=True)
    def post(self):
        """
        视type类型决定加减,0为售出,非0为进货
        """
        id = api.payload['goods_id']
        nums = api.payload['change_num']
        type= api.payload['type']
        if type :
            return goods_Replenish(id,nums)
        return goods_sell(id,nums)
@api.route('/low')
class low(Resource):
    @api.doc(description='显示数量过低的商品')
    def post(self):
        """
        显示所有数量小于标准持有量的商品
        """
        return goods_nums_verify()
@api.route('/show')
class show(Resource):
    @api.doc(description='展示商品')
    def post(self):
        '''
        显示商品列表
        '''
        return goods_show()
@api.route('/record')
class sale_record(Resource):
    @api.doc(description='展示销售记录')
    def post(self):
        '''
        显示销售记录
        '''
        return show_sale_record()
@api.route('/delete')
class sale_record(Resource):
    @api.doc(description='删除对应id商品')
    @api.expect(delete_model, validate=True)
    def post(self):
        '''
        商品删除
        '''
        if (current_user.power >>2) &1 :  # type: ignore
            id = api.payload['goods_id']
            return goods_delete(id)
        return {'message': '当前用户不具有将商品下架的权限'}, 403     
@api.route('/update')
class update(Resource):
    @api.doc(description='商品数据更改')
    def post(self):
        '''
        对商品数据进行修改
        '''
        if (current_user.power >>1) &1 :  # type: ignore
            
            goods_id = api.payload['id']
            new_data = api.payload['new_data']
            return  goods_conifg(goods_id ,new_data)
        return {'message': '当前用户不具有修改商品信息的权限'}, 403     

@api.errorhandler
def handle_validation_error(error):
    return {'message': 'Validation failed', 'error': str(error)}, 410
