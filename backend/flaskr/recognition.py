from flask_restx import Namespace, Resource , fields   # RESTful API
# from function.recognition import image_to_mongo,data_from_mongo,image_delete_mongo,tranform,img_clear,image_read,image_from_video，
from function.recognition import  * 
from flaskr.extensions import socketio
from instance.yolo_config import path_config
import base64
import cv2
import json
api = Namespace('recognition', description='识别接口')
label_model = api.model('labelmodel', {
    'label_name': fields.String(max_length=100, required=True, description='标签名称'),
})

@api.route('/add')
class add(Resource):
    @api.doc(description='显示数量过低的商品')
    @api.expect(label_model, validate=True)
    def post(self):
        """
        添加数据至mongo
        """
        name = api.payload['label_name']
        return image_to_mongo(name)

@api.route('/get')
class get(Resource):
    @api.doc(description='获取')
    def post(self):
        """
        获取数据
        """
        return data_from_mongo()
    
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
    
@api.route('/trans')
class trans(Resource):
    @api.doc(description='')
    def post(self):
        """
        """
        return tranform()
    
@api.route('/clear')
class clear(Resource):
    @api.doc(description='')
    def post(self):
        """
        """
        return img_clear()
    
@api.route('/write')
class read(Resource):
    @api.doc(description='')
    @api.expect(label_model, validate=True)
    def post(self):
        """
        """
        name = api.payload['label_name']
        img_list_withpath = image_from_video()
        return image_read(img_list_withpath,name)
    
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
    print("tq2qadffqef")
    cap = cv2.VideoCapture(int(source))
    while cap.isOpened() and connected:
        success, frame = cap.read()
        frame = detect_goods(frame)
        frame = base64(frame)
        data =  {
            'frame' : frame,
        }
        result = json.dumps(data)
        socketio.emit('receive',result)  

    cap.release()
