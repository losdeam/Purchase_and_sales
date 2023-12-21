from ultralytics import YOLO
import yaml
import cv2 
import time 
from instance.yolo_config import path_config
# file_path,
# 加载预训练的YOLOv8n模型

model_path = path_config['model_path']
model = YOLO(model_path)
source= path_config['source_path']

def detect_goods(img):
    results = model(img, imgsz=640, conf=0.3)
# 在帧上可视化结果
    annotated_frame = results[0].plot()
    return annotated_frame




    
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