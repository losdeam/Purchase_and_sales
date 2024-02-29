from flask_restx import Namespace, Resource , fields   # RESTful API
# from function.recognition import  clear_all 
# from 
from function.util import *
import base64
import cv2
import time 
from ultralytics import YOLO
import yaml
import subprocess






# 定义请求解析器

api = Namespace('test', description='测试接口')

change_model = api.model('changemodel',{
    'goods_id': fields.Integer(required=True, description='商品id'),
    'change_num': fields.Integer(required=True, description='商品售出/进货数量'),
    'type': fields.Integer(required=True, description='商品售出/进货类型')

})
delete_model = api.model('deletemodel',{
    'goods_id': fields.Integer(required=True, description='商品id'),
})
label_model = api.model('labelmodel', {
    'label_name': fields.String(max_length=100, required=True, description='标签名称'),
})
@api.route('/init')

class init(Resource):
    @api.doc(description='删除')

    def post(self):
        """
        初始化
        """
        clear_all()
        return data_init()
#-----------识别部分-----------
@api.route('/mongo_delete')
class mongo_delete(Resource):
    def post(self):
        """
        """
        val_script_path = get_config_data('path_config','val_script_path') 
        source_model_path = get_config_data('path_config','source_model_path')
        subprocess.run(['python', val_script_path,source_model_path])
        name = api.payload['label_name']
        return image_delete_mongo(name)
@api.route('/val_script')
class val_script(Resource):
    def post(self):
        """
        """
        yaml_path = get_config_data('path_config','yaml_path')
        val_script_path = get_config_data('path_config','val_script_path') 
        source_model_path = get_config_data('path_config','source_model_path')
        output = subprocess.run(['python', val_script_path,source_model_path,yaml_path])
        print(type(output),output.__dir__())
        return 
@api.route('/local_delete')
class local_delete(Resource):
    @api.doc(description='删除')

    def post(self):
        """
        删除mongo对应标签数据
        """
        return img_clear()

@api.route('/clear')
class clear(Resource):
    @api.doc(description='将所有的训练数据清空')
    def post(self):
        """
        清空训练，从零开始
        """
        # 清空本地文件

        image_delete_local(get_config_data('path_config','video_file_path'))
        image_delete_local(get_config_data('path_config','image_file_path'))
        image_delete_local(get_config_data('path_config','label_file_path'))
        image_delete_local(get_config_data('path_config','model_file_path'))
        image_delete_local(get_config_data('path_config','yaml_file_path'))
        # 清空mongo中的数据
        image_delete_mongo_all()

        yaml_clear(get_config_data('path_config','yaml_path'))    
        # 
        return "清空完毕"


#----------------------
goods_model = api.model('goods_model', {
    "name" :fields.String(max_length=30, required=True, description='商品名称'),
    "num" : fields.Integer(max_length=30, required=True, description='商品数量'),
    "price_buying" : fields.Float(max_length=30, required=True, description='商品进货价格'),
    "price_retail" : fields.Float(max_length=30, required=True, description='商品零售价格'),
    "baseline" : fields.Integer(max_length=100, required=True, description='商品基准量'),
})

user_model = api.model('user_model', {
    "name" :fields.String(max_length=30, required=True, description='用户名称'),
    "password" : fields.String(max_length=30, required=True, description='用户密码'),
    "rank" : fields.Float(max_length=30, required=True, description='用户是否为管理员'),
    "power" : fields.Float(max_length=30, required=True, description='用户的操作权限'),
})

#----------mongo-------


@api.route('/mongo_data_get')
class mongo_data_get(Resource):
    @api.doc(description='')
    def post(self):
        """
        向mongo中添加数据
        """
        return data_from_mongo('goods')
    
@api.route('/mongo_find_')
class mongo_data_find(Resource):
    @api.doc(description='')
    def post(self):
        """
        
        """
        return data_find_mongo('goods','id',1)


# @api.route('/mongo_drop')
# class mongo_drop(Resource):
#     @api.doc(description='')
#     def post(self):
#         """
#         向mongo中添加数据
#         """
#         return data_from_mongo('goods')
# -----------------------------------
    


# --------------------yaml--------
user_model = api.model('path_model', {
    "path" :fields.String(max_length=30, required=True, description='路径'),
})
@api.route('/yaml_read_')
class yaml_read_(Resource):
    @api.expect(user_model, validate=True)
    @api.doc(description='')
    def post(self):
        """
        向mongo中添加数据
        """
        path = api.payload['path']
        return yaml_read(path)
    
from function.goods import goods_add,goods_delete_f
import random
import string
import datetime
@api.route('/goods_data_add')
class goods_data_add(Resource):
    def post(self):
        """
        添加商品数据
        """
        category = ['category1','category2','category3','category4','category5']
        for i in range(20):
            characters = string.ascii_letters + string.digits
            goods_name = ''.join(random.choice(characters) for _ in range(6))

            goods_num = int(random.random()*50 +1) 
            goods_price_buying = random.random() * 50
            goods_price_retail = goods_price_buying +1 
            goods_category = category[int(random.random() *5) ]
            goods_baseline = goods_num +1 

            data_sql = goods_add(goods_name ,goods_num,goods_price_buying,goods_price_retail,goods_category,goods_baseline)
        # return  '添加完毕'
@api.route('/goods_data_clear')
class goods_data_clear(Resource):
    def post(self):
        """
        清空商品数据
        """
        goods_id_list = redis_client.hkeys('goods_data')
        for goods_id in goods_id_list:
            goods_delete_f(int(goods_id))
@api.route('/reord_data_clear')
class reord_data_clear(Resource):
    def post(self):
        """
        清空销售记录
        """
        data_delete_mongo(None,None ,'sales_records')
@api.route('/goods_data_clear')
class reord_data_clear(Resource):
    def post(self):
        """
        清空商品
        """
        data_delete_mongo(None,None ,'goods_data')
@api.route('/reord_data_add')
class reord_data_add(Resource):
    def post(self):
        """
        添加销售记录
        """
        goods_id_list = redis_client.hkeys('goods_data')
        for goods_id in goods_id_list:
            for day in range(7):
                goods_id = int(goods_id)
                nums = 50 -day*(goods_id % 3 - 1 )*3
                message,flag = data_to_mongo("sales_records",{'time_stamp' : datetime.datetime.now()+datetime.timedelta(days=day),\
                                            'records_data' : {goods_id:nums}
                })
                print(message,flag )
