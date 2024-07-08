from flask_restx import Namespace, Resource , fields   # RESTful API
# from function.recognition import image_to_mongo,image_from_mongo,image_delete_mongo,tranform,img_clear,image_read,image_from_video，
from function.recognition import  * 
from function.goods import goods_delete_f
from function.util import data_get_mongo,get_config_data,yaml_detele
from flaskr.extensions import socketio,redis_client,logging,train_queue
from flask import request,jsonify
from flask_login import current_user
# from instance.yolo_config import path_config
from ultralytics import YOLO
import collections
import base64
import cv2
import time 
import datetime

api = Namespace('recognition', description='识别接口')
label_model = api.model('labelmodel', {
    'label_name': fields.String(max_length=100, required=True, description='标签名称'),
})



@api.route('/train')
class train(Resource):
    @api.doc(description='一台设备仅支持同时调用一次该接口，否则可能会出现报错')
    def post(self):
        """
        模型训练
        """
        #--------------------参数输入--------------
        arg_name =  ('商品视频',"背景图",'商品id')
        try:
            goods_video = request.files['goods_video']
            bg_img = request.files['bg_img']
            goods_id = int(request.form['goods_id'])
        except Exception as e: 
            goods_delete_f(goods_id)
            result = jsonify({'message': '获取背景图与商品视频时出现问题'})
            result.status_code = 401  
            logging[current_user.rank].append(f"{datetime.datetime.now()}-----{current_user.name}-----下架id为{id}的商品失败,原因为当前用户不具有将商品下架的权限")
            return result
        #----------------------------------
        #--------------------空值检测--------------
        pras = (goods_video,bg_img,goods_id)
        for index,i in enumerate(pras):
            if not i :
                result = jsonify({'message': f'{arg_name[index]}未填写'})
                result.status_code = 402  
                return result 
        #----------------------------------
        # 获取训练数据（缺乏mongo中保存与提取机制，尚不支持队列训练）
        message,config = config_read(goods_id,bg_img,goods_video) 
        train_queue.append(config)
        # print(train_queue)
        result = jsonify({'message': f'已将商品{goods_id}加入训练队列'})
        result.status_code = 200  
        return result 


            

        


@api.route('/get_data')
class get_datas(Resource):
    @api.doc(description='')
    @api.expect(label_model, validate=True)
    def post(self):
        """
        获取数据
        """
        label = api.payload['label_name']

        return get_data(label)
    
@api.route('/strengthen')
class strengthen(Resource):
    @api.doc(description='')
    def post(self):
        """
        模型强化
        """
        
        return train_strengthen()
    
# @api.route('/confirm_recognition')
# class confirm(Resource):
#     @api.doc(description='')
#     def post(self):
#         """
#         模型强化
#         """
#         return train_strengthen()

####### 连接部分 #########
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
    source = get_config_data('path_config','source_path')
    try:
        model = YOLO(get_config_data('path_config','source_model_path'))
    except Exception as e :
        # print(e)
        model = YOLO(get_config_data('path_config','origin_model_path'))
    cap = cv2.VideoCapture(int(source))
    while cap.isOpened() and connected:
        success, frame = cap.read()
        if not success :
            time.sleep(1)
            break 
        
        data_result = detect_goods(model,frame)
        recognize_data = get_goods_data(data_result)
        _, buffer = cv2.imencode('.jpg', data_result['image'])
        base64_frame = base64.b64encode(buffer).decode('utf-8')
        if connected:
            socketio.emit('receive',        data =  {
                'frame' : base64_frame,
                'message':recognize_data
            })  
    cap.release()


            
        #--------------------训练模块--------------
# @socketio.on('sent_message') 
# def disconnect ():