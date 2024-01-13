from flask_restx import Namespace, Resource , fields   # RESTful API
# from function.recognition import  clear_all 
# from 
from function.util import *
from instance.yolo_config import path_config,data_config,data_config
import base64
import cv2
import time 
from ultralytics import YOLO
import yaml







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
    @api.doc(description='删除')
    @api.expect(label_model, validate=True)
    def post(self):
        """
        删除mongo对应标签数据
        """
        name = api.payload['label_name']
        return image_delete_mongo(name)

@api.route('/local_delete')
class local_delete(Resource):
    @api.doc(description='删除')

    def post(self):
        """
        删除mongo对应标签数据
        """
        return img_clear()
# @api.route('/get_data_video')
# class get_data_video(Resource):
#     @api.expect(label_model, validate=True)
#     @api.doc(description='从video文件的视频中获取图像')
#     def post(self):
#         """
#         添加图像-视频
#         """
#         label = api.payload['label_name']
#         bg_path = path_config['bg_imgfile_path'] 
#         bg  = cv2.imread(bg_path)
        
#         img_clear()
#         img_list_withpath = image_from_video(data_config['target_frame_count'])
#         image_read(img_list_withpath,label,bg,test= True)
#         return "成功从视频中添加图像数据"
  
@api.route('/get_data_mongo')
class get_data_mongo(Resource):
    @api.doc(description='从mongo中获取已使用过的图像')
    def post(self):
        """
        添加图像-mongo
        """
        return image_from_mongo(data_config['sample_size'])

@api.route('/image_operation_center')
class image_operation_center(Resource):
    @api.doc(description='对images中已有图像进行处理，获取其聚类中心，并添加标签')
    def post(self):
        """
        图像处理-获取商品位置
        """
        return image_from_mongo(data_config['sample_size'])
    
# @api.route('/image_operation_split')
# class image_operation_split(Resource):
#     @api.doc(description='对images中已有图像进行处理，进行训练集以及验证集的划分')
#     def post(self):
#         """
#         图像处理-图像划分
#         """
#         return SplitDataset()

# @api.route('/train')
# class train(Resource):
#     @api.doc(description='一台设备仅支持同时调用一次该接口，否则可能会出现报错')
#     @api.expect(label_model, validate=True)
#     def post(self):
#         """
#         模型训练
#         """
#         label = api.payload['label_name']
#         return train_new_label(label)
@api.route('/clear')
class clear(Resource):
    @api.doc(description='将所有的训练数据清空')
    def post(self):
        """
        清空训练，从零开始
        """
        # 清空本地文件
        image_delete_local(path_config['video_path'])
        image_delete_local(path_config['image_path'])
        image_delete_local(path_config['label_path'])
        image_delete_local(path_config['model_file_path'])

        # 清空mongo中的数据
        image_delete_mongo_all()

        yaml_clear()    
        # 
        return "清空完毕"

# @api.route('/detect_local')
# class detect(Resource):
#     @api.doc(description='一台设备仅支持同时调用一次该接口，否则可能会出现报错')
#     def post(self):
#         """
#         进行检测并在本地调用窗口进行播放
#         """
#         return detect_local()

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
@api.route('/goods_data_add')
class mongo_data_add(Resource):
    @api.expect(goods_model, validate=True)
    @api.doc(description='')
    def post(self):
        """
        向mongo中添加数据
        """
        name = api.payload['name']
        num = api.payload['num']
        price_buying = api.payload['price_buying']
        price_retail = api.payload['price_retail']
        baseline = api.payload['baseline']
        return data_to_mongo("goods",{"name":name,\
                                "num" : num,
                                "price_buying" : price_buying,
                                "price_retail" : price_retail,
                                "baseline" : baseline,})

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