from flask_restx import Namespace, Resource , fields   # RESTful API
from function.recognition import  * 
from function.goods import good_add,good_sell,good_nums_verify,good_Replenish,good_show,show_sale_record,good_delete,good_conifg
from flaskr.extensions import socketio
from flaskr.extensions import db ,redis_client      # 导入数据库
from flask_login import logout_user, login_required, current_user  # 用户认证
from flask import request,jsonify
from instance.yolo_config import path_config,train_config,image_config
import base64
import cv2
import time 
from ultralytics import YOLO
import yaml

import flaskr.models  # 务必导入模型





# 定义请求解析器

api = Namespace('test', description='测试接口')

change_model = api.model('changemodel',{
    'good_id': fields.Integer(required=True, description='商品id'),
    'change_num': fields.Integer(required=True, description='商品售出/进货数量'),
    'type': fields.Integer(required=True, description='商品售出/进货类型')

})
delete_model = api.model('deletemodel',{
    'good_id': fields.Integer(required=True, description='商品id'),
})
label_model = api.model('labelmodel', {
    'label_name': fields.String(max_length=100, required=True, description='标签名称'),
})
#-----------识别部分-----------
@api.route('/get_data_video')
class get_data_video(Resource):
    @api.expect(label_model, validate=True)
    @api.doc(description='从video文件的视频中获取图像')
    def post(self):
        """
        添加图像-视频
        """
        label = api.payload['label_name']
        bg_path = path_config['bg_imgfile_path'] 
        bg  = cv2.imread(bg_path)
        
        img_clear()
        img_list_withpath = image_from_video(image_config['target_frame_count'])
        image_read(img_list_withpath,label,bg,test= True)
        return "成功从视频中添加图像数据"
  
@api.route('/get_data_mongo')
class get_data_mongo(Resource):
    @api.doc(description='从mongo中获取已使用过的图像')
    def post(self):
        """
        添加图像-mongo
        """
        return data_from_mongo(train_config['sample_size'])

@api.route('/image_operation_center')
class image_operation_center(Resource):
    @api.doc(description='对images中已有图像进行处理，获取其聚类中心，并添加标签')
    def post(self):
        """
        图像处理-获取商品位置
        """
        return data_from_mongo(train_config['sample_size'])
    
@api.route('/image_operation_split')
class image_operation_split(Resource):
    @api.doc(description='对images中已有图像进行处理，进行训练集以及验证集的划分')
    def post(self):
        """
        图像处理-图像划分
        """
        return SplitDataset()

@api.route('/train')
class train(Resource):
    @api.doc(description='一台设备仅支持同时调用一次该接口，否则可能会出现报错')
    @api.expect(label_model, validate=True)
    def post(self):
        """
        模型训练
        """
        label = api.payload['label_name']
        return train_new_label(label)
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

        # 清空yaml中数据
        yaml_path = path_config['yaml_path']
        with open(yaml_path, 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        # 修改指定键的值
        data['names'] = []
        data['nc'] = 0
        # 写入修改后的内容回到文件
        with open(yaml_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)
        
        # 
        return "清空完毕"

@api.route('/detect_local')
class detect(Resource):
    @api.doc(description='一台设备仅支持同时调用一次该接口，否则可能会出现报错')
    def post(self):
        """
        进行检测并在本地调用窗口进行播放
        """
        return detect_local()

#----------------------
#-----------连接部分-----------
connected = False 
@socketio.on('connect') 
# 当连接完毕
def connect():
    global connected
    connected = True 
# 当连接断开
@socketio.on('disconnect') 
def disconnect ():
    global connected
    connected = False


@socketio.on('sent_img') 
def sent():
    source = path_config['source_path']
    try:
        model = YOLO(path_config['model_path'])
    except:
        model = YOLO(path_config['origin_model_path'])
    cap = cv2.VideoCapture(int(source))
    while cap.isOpened() and connected:
        success, frame = cap.read()
        if not success :
            time.sleep(1)
            continue 

        frame = detect_goods(model,frame)
        _, buffer = cv2.imencode('.jpg', frame)
        base64_frame = base64.b64encode(buffer).decode('utf-8')
        if connected:
            socketio.emit('receive',        data =  {
                'frame' : base64_frame,
            })  
    cap.release()

@socketio.on('sent_message') 
def sent_message ():
    global connected
    connected = False

#------------------------------
