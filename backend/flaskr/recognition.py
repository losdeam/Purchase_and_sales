from flask_restx import Namespace, Resource , fields   # RESTful API
# from function.recognition import image_to_mongo,data_from_mongo,image_delete_mongo,tranform,img_clear,image_read,image_from_video，
from function.recognition import  * 
from function.goods import good_delete_f
from flaskr.extensions import socketio
from flask import request,jsonify
from instance.yolo_config import path_config
from ultralytics import YOLO
import base64
import cv2
import time 
import json
api = Namespace('recognition', description='识别接口')
label_model = api.model('labelmodel', {
    'label_name': fields.String(max_length=100, required=True, description='标签名称'),
})


@api.route('/delete')
class delete(Resource):
    @api.doc(description='获取')
    @api.expect(label_model, validate=True)
    def post(self):
        """
        删除mongo对应标签数据
        """
        name = api.payload['label_name']
        return image_delete_mongo(name)


    
@api.route('/train')
class train(Resource):
    @api.doc(description='一台设备仅支持同时调用一次该接口，否则可能会出现报错')
    def post(self):
        """
        模型训练
        """
        arg_name =  ('商品视频',"背景图",'商品id')
        #--------------------参数输入--------------
        try:
            good_video = request.files['good_video']
            bg_img = request.files['bg_img']
            good_id = int(request.form['good_id'])
        except Exception as e: 
            result = jsonify({'message': '获取背景图与商品视频时出现问题'})
            result.status_code = 401  
            return result
        
        #--------------------训练模块--------------
        #----------------------------------
        #--------------------空值检测--------------
        pras = (good_video,bg_img,good_id)
        for index,i in enumerate(pras):
            if not i :
                result = jsonify({'message': f'{arg_name[index]}未填写'})
                result.status_code = 402  
                return result 
        #----------------------------------
        #--------------------训练模块--------------
        try:
            data_train = train_new_label(good_id,bg_img,good_video)
            if data_train['code'] != 200 :
                good_delete_f(good_id)
            result = jsonify(data_train)
            result.status_code = data_train['code']
            return result
        except Exception as e :
            result = jsonify({'message': '出现错误致使程序中断'})
            result.status_code = 404
            return result

        #--------------------训练模块--------------



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
source = path_config['source_path']
@socketio.on('sent_img') 
def sent():
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
# @socketio.on('sent_message') 
# def disconnect ():