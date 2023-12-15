import random
import os 
import base64
import shutil
import cv2 

from instance.yolo_config import path_config,image_config
from flaskr.extensions import mongo
from function.sql import get_all
from .util import SplitDataset
image_path = path_config["image_path"]
lable_path = path_config["lable_path"]
num_images_to_select = image_config['sample_size']
target_frame_count = image_config['target_frame_count'] # 从视频中获取的图像数量
video_path = ""

def image_delete_mongo(label):
    """
    删除mongo中数据
    """
    collection = mongo.db.image_data

    # 构建删除条件
    query = {"label": label}

    # 删除具有特定字段值的所有记录
    result = collection.delete_many(query)
    # 返回删除的记录数量
    return {'deleted_count': result.deleted_count}
def image_delete_local(folder_path):
    """
    删除本地数据
    """
        # 检查文件夹是否存在
    if os.path.exists(folder_path):
        # 获取文件夹下的所有文件和子文件夹
        items = os.listdir(folder_path)

        # 删除文件夹下的所有文件和子文件夹
        for item in items:
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)

        print(f"文件夹 '{folder_path}' 已清空。")
    else:
        print(f"文件夹 '{folder_path}' 不存在。")
def image_to_mongo(label):
    """
    将训练数据保存至mongo数据库中
    """
    
    data = {}
    data["message"] = []
    collection = mongo.db.image_data
    list_image_path = os.listdir(image_path)
    for image_name  in list_image_path:
        image_path_single = image_path +"/"+ image_name
        lable_path_single = lable_path +"/"+ image_name[:-4] + ".txt"
        with open(image_path_single, 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read())
        with open(lable_path_single, 'rb') as lable_file:
            content = lable_file.read()
        document = {'image':encoded_image,"name":image_name,"label_txt":content,"label":label}
        collection.insert_one(document)
    data["message"].append("添加完毕")
    image_delete_local(image_path)
    image_delete_local(lable_path)
    return data
def image_from_mongo():
    """
    从mongo中随机提取数据   
    """
    img_clear()
    collection = mongo.db.image_data
    good_names = get_all("good_name","goods")
    good_names.append("string")
    good_names.append("fall")
    n =0 

    for good_name in good_names:
        pipeline = {'label' :good_name}
        result = collection.find(pipeline)
        list_result = list(result)
        selected_images = random.sample(list_result, min(num_images_to_select, len(list_result)))
        for record in selected_images:
            image_data = base64.b64decode(record['image'])
            with open(image_path +"/"+record["name"], 'wb') as image_file:
                image_file.write(image_data)
            with open(lable_path +"/"+record["name"][:-4] + ".txt", 'wb') as label_file:
                label_file.write(record['label_txt'])
        n +=len(selected_images)
    data = {}
    data["count"] = n
    SplitDataset()
    return data
def img_clear():
    image_delete_local(image_path)
    image_delete_local(lable_path)
def image_from_video(video_path,output_folder, target_frame_count):
    '''
    从视频中获取图像数据，并保存至文件夹中
    '''
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    capture_interval = int(total_frames / target_frame_count)

    # 创建输出文件夹
    os.makedirs(output_folder, exist_ok=True)

    # 开始截取图像
    frame_count = 0
    while frame_count < target_frame_count:
        ret, frame = cap.read()
        if not ret:
            break  # 视频读取结束
        # 每隔一定帧数截取一帧
        if frame_count % capture_interval == 0:
            output_path = os.path.join(output_folder, f"frame_{frame_count // capture_interval}.jpg")
            cv2.imwrite(output_path, frame)
        frame_count += 1
    # 释放视频捕捉对象
    cap.release()

