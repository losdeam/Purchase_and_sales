# from ultralytics import YOLO
# from instance.yolo_config import path_config
from flaskr.extensions  import redis_client
import cv2
import time 
import json


def get_goods_data(detect_data):
    '''
    获取json数据
    input: 
        detect_data : 识别获取的商品数据
    
    '''
    recognize_data = []
    temp_dict = {}
    for goods_id in detect_data['label']:
        if goods_id in temp_dict:
            temp_dict[goods_id]['goods_count'] += 1 
        else:
            goods_data = redis_client.hget('goods_data', goods_id)
            if goods_data:
                goods_data_dict  = json.loads(goods_data)
                temp_dict[goods_id] = {}
                temp_dict[goods_id]['goods_id'] =  goods_id
                temp_dict[goods_id]['goods_name'] =  str(goods_data_dict['name'])
                temp_dict[goods_id]['goods_count'] = 1
                temp_dict[goods_id]['goods_price'] = float(goods_data_dict['price_retail'])
    for goods_id in temp_dict:
        recognize_data.append(temp_dict[goods_id])
    

    return recognize_data

def detect_goods(model,img):
    '''
    根据输入的模型检测img中的对应物体
    input :
        model: 已经载入完毕的YOLO模型
        img : 图像
    output:
        annotated_frame: 带识别标记的图像
    '''
    data_result = {}
    data_result['label'] = []
    data_result['conf'] =[]
    data_result['site'] =[]

    dict_label = None 
    if img.any :
        results = model(source=img, imgsz=320, conf=0.5,iou= 0.5)
    # 在帧上可视化结果  
        annotated_frame = results[0].plot()
        if not dict_label:
            dict_label = results[0].names
        for x_min,y_min,x_max,y_max,conf,label in results[0].boxes.data:
            # print(int((x_max-x_min)),int((y_max-y_min)),int((x_max-x_min) * (y_max-y_min)),int(label))
            if int((x_max-x_min) * (y_max-y_min))> 640** 2  * 0.8  : 
                continue 
            x_min,y_min,x_max,y_max,label = map(int,(x_min,y_min,x_max,y_max,label))
            conf = float(conf)
            data_result['label'].append(dict_label[label])
            data_result['conf'].append(conf)
            data_result['site'].append((x_min,y_min,x_max,y_max))
        data_result['image'] = annotated_frame
        return data_result
# source = path_config['source_path']
# def detect_local():

#     try:
#         model = YOLO(path_config['model_path'])
#     except:
#         model = YOLO(path_config['origin_model_path'])
#     cap = cv2.VideoCapture(int(source))
#     while cap.isOpened() :
#         success, frame = cap.read()
#         dict_label = {}
#         data_result = {}
#         data_result['label'] = []
#         data_result['conf'] =[]
#         data_result['site'] =[]
#         if not success :
#             time.sleep(1)
#             break 
#         if frame.any :
#             results = model(source=frame, imgsz=320,  conf=0.4,iou= 0.7)
#         # 在帧上可视化结果
#             if not dict_label:
#                 dict_label = results[0].names
#             for x_min,y_min,x_max,y_max,conf,label in results[0].boxes.data:
#                 print(int((x_max-x_min)),int((y_max-y_min)),int((x_max-x_min) * (y_max-y_min)),int(label))
#                 if int( (x_max-x_min)* (y_max-y_min))> (640*0.4)** 2 : 
#                     continue 
                
#                 x_min,y_min,x_max,y_max,label = map(int,(x_min,y_min,x_max,y_max,label))
#                 conf = float(conf)
#                 data_result['label'].append(dict_label[label])
#                 data_result['conf'].append(conf)
#                 data_result['site'].append((x_min,y_min,x_max,y_max))
#             annotated_frame = results[0].plot()
#             cv2.imshow("local",annotated_frame)
#             if not dict_label:
#                 dict_label = results[0].names
#             recognize_data = get_goods_data(data_result)
#             print(recognize_data)  
            
#         if cv2.waitKey(1) &  0xff == ord("q"): # 在英文状态下，按下按键 q 会关闭显示窗口    
#             break
#     cap.release()
#     return "结束"

    
# # # 在'bus.jpg'上运行推理，并附加参数
# results = model.predict(source, imgsz=320, conf=0.5,stream= True)
# for i in results:
#     for box in i.boxes.xyxy:
#         x_min,y_min,x_max,y_max = map(int,box)
#         # print(x_min,x_max,y_min,y_max)
#         img = i.orig_img[y_min:y_max,x_min:x_max]
#         # print(img)
#     cv2.imshow("orig",i.orig_img)
#     cv2.waitKey(0)