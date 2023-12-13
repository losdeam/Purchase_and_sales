from ultralytics import YOLO
import cv2 
from setting import setting

# 加载预训练的YOLOv8n模型
model = YOLO(setting['model_path'])
source= setting['source_path']
def get_video():
    # 视频流判断
    if type(source) == str and "\\" not in source:
        cap = cv2.VideoCapture(int(source))
        while cap.isOpened():
            # 从视频中读取一帧
            success, frame = cap.read()
            if success:
                # 在该帧上运行YOLOv8推理
                results = model(frame)
                # 在帧上可视化结果
                annotated_frame = results[0].plot()
                # 显示带注释的帧
                cv2.imshow("YOLOv8推理", annotated_frame)
                # 如果按下'q'则中断循环
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                # 如果视频结束则中断循环
                break

        # 释放视频捕获对象并关闭显示窗口
        cap.release()
        cv2.destroyAllWindows()
    else:
        results = model.predict(source, imgsz=320, conf=0.5,stream= True)
        for i in results:
            annotated_frame = i.plot()
            for box in i.boxes.xyxy:
                
                x_min,y_min,x_max,y_max = map(int,box)
                img = i.orig_img[y_min:y_max,x_min:x_max]
            cv2.imshow("orig",annotated_frame)
            cv2.waitKey(0)
def add_new_goods(good_name ):
    '''
    将商品名称添加到配置文件中，以便于进行训练
    '''
    pass 

get_video()

        

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