from ultralytics import YOLO
from instance.yolo_config import path_config
import cv2
import time 
# file_path,
# 加载预训练的YOLOv8n模型




def detect_goods(model,img):
    '''
    根据输入的模型检测img中的对应物体
    input :
        model: 已经载入完毕的YOLO模型
        img : 图像
    output:
        annotated_frame: 带识别标记的图像
    '''

    if img.any :
        results = model(source=img, imgsz=320, conf=0.5)
    # 在帧上可视化结果
        annotated_frame = results[0].plot()
        return annotated_frame
source = path_config['source_path']
def detect_local():
    try:
        model = YOLO(path_config['model_path'])
    except:
        model = YOLO(path_config['origin_model_path'])
    cap = cv2.VideoCapture(int(source))
    while cap.isOpened() :
        success, frame = cap.read()
        if not success :
            time.sleep(1)
            continue 
        if frame.any :
            results = model(source=frame, imgsz=320, conf=0.3)
        # 在帧上可视化结果
            annotated_frame = results[0].plot()
            cv2.imshow("local",annotated_frame)
        if cv2.waitKey(1) &  0xff == ord("q"): # 在英文状态下，按下按键 q 会关闭显示窗口    
            break



    
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