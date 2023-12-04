from flask_restx import Namespace, Resource , fields   # RESTful API
from flaskr.extensions import db ,redis_client      # 导入数据库
from function.goods import good_add,good_sell,good_nums_verify,good_Replenish,good_show,show_sale_record,good_delete,good_conifg
import flaskr.models  # 务必导入模型
import datetime 
api = Namespace('goods', description='商品操作接口')
add_model = api.model('addmodel', {
    'Warehouse_id':fields.Integer(required=True, description='所存储的仓库的编号'),
    'good_name': fields.String(max_length=100, required=True, description='商品名称'),
    'good_num': fields.Integer(required=True, description='商品库存数量'),
    'good_price_buying': fields.Float(required=True, description='商品进货价格'),
    'good_price_retail': fields.Float(required=True, description='商品零售价格'),
    'good_sort': fields.String(max_length=100, required=True, description='商品分类'),
    'good_baseline': fields.Integer(required=True, description='商品最低库存量'),
    'good_note' : fields.String(max_length=200, required=True, description='商品备注'),
})

change_model = api.model('changemodel',{
    'good_id': fields.Integer(required=True, description='商品id'),
    'change_num': fields.Integer(required=True, description='商品售出/进货数量'),
    'type': fields.Integer(required=True, description='商品售出/进货类型')
})
delete_model = api.model('deletemodel',{
    'good_id': fields.Integer(required=True, description='商品id'),
})
@api.route('/add')
class add(Resource):
    @api.doc(description='全新商品购入')
    @api.expect(add_model, validate=True)
    def post(self):
        '''
        全新商品购入
        '''
        Warehouse_id = api.payload['Warehouse_id']
        good_name = api.payload['good_name']
        good_num = api.payload['good_num']
        good_price_buying = api.payload['good_price_buying']
        good_price_retail = api.payload['good_price_retail']
        good_sort = api.payload['good_sort']
        good_baseline = api.payload['good_baseline']
        good_note = api.payload['good_note']
        
        return  good_add(Warehouse_id,good_name ,good_num,good_price_buying,good_price_retail,good_sort,good_baseline,good_note)

@api.route('/change')
class Replenish(Resource):
    @api.doc(description='商品数量改变')
    @api.expect(change_model, validate=True)
    def post(self):
        """
        视type类型决定加减,0为售出,非0为进货
        """
        id = api.payload['good_id']
        nums = api.payload['change_num']
        type= api.payload['type']
        if type :
            return good_Replenish(id,nums)
        return good_sell(id,nums)
    
@api.route('/low')
class low(Resource):
    @api.doc(description='显示数量过低的商品')
    def post(self):
        """
        显示所有数量小于标准持有量的商品
        """
        return good_nums_verify()


@api.route('/show')
class show(Resource):
    @api.doc(description='展示商品')
    def post(self):
        '''
        '''
        return good_show()

@api.route('/record')
class sale_record(Resource):
    @api.doc(description='展示销售记录')
    def post(self):
        '''
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
        id = api.payload['good_id']
        return good_delete(id)
    
@api.route('/update')
class update(Resource):
    @api.doc(description='商品数据更改')
    def post(self):
        '''
        '''
        good_id = api.payload['good_id']
        new_data = api.payload['new_data']
        return  good_conifg(good_id ,new_data)