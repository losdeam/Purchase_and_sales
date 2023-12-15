from ultralytics import YOLO
import yaml
import cv2 
import time 
from instance.yolo_config import path_config
# file_path,
# 加载预训练的YOLOv8n模型
model = YOLO(path_config['model_path'])
source= path_config['source_path']
yaml_path = path_config["yaml_path"]
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
def add_new_goods(good_id ):
    '''
    将商品名称添加到配置文件中，以便于进行训练
    '''
    # 读取 YAML 文件
    with open(yaml_path, 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    # 修改指定键的值
    if good_id in data['names']:
        return f"商品{good_id}已经存在"
    data['names'].append(good_id)
    data['nc'] = len(data['names'])

    # 写入修改后的内容回到文件
    with open(yaml_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)
    return f"修改成功"
def delete_goods(good_id):
    '''
    删除商品时删除对应标签
    '''

    # 读取 YAML 文件
    with open(yaml_path, 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)

    # 修改指定键的值
    if good_id not in data['names']:
        return f"商品{good_id}不存在"
    data['names'].pop(data['names'].index(good_id))
    data['nc'] -=1 

    # 写入修改后的内容回到文件
    with open(yaml_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

    return f"{good_id}号商品删除成功"



    
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