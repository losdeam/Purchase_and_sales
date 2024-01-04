
import random
import os 
import base64
import shutil
import cv2 
import numpy as np
import time 

from instance.yolo_config import path_config,image_config
from flaskr.extensions import mongo
from function.sql import get_all

image_flie_path = path_config["image_path"]
label_flie_path = path_config["label_path"]
video_flie_path = path_config["video_path"]
target_frame_count = image_config['target_frame_count'] 
img_size = image_config['img_size']
goods_imgfile_path = path_config['goods_imgfile_path'] 

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
def image_delete_mongo_all():
    """
    删除mongo中数据
    """
    collection = mongo.db.image_data
    # 删除具有特定字段值的所有记录
    result = collection.drop()
    # 返回删除的记录数量
    return {'message': "mongo中的数据清理完毕"}
def image_to_mongo(label):
    """
    将训练数据保存至mongo数据库中
    """
    data = {}
    data["message"] = []
    collection = mongo.db.image_data

    for image_name  in range(target_frame_count):
        image_path_single = image_flie_path +"/"+ str(image_name) + ".jpg"
        label_path_single = label_flie_path +"/"+ str(image_name) + ".txt"
        with open(image_path_single, 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read())
        with open(label_path_single, 'rb') as label_file:
            content = label_file.read()
        document = {'image':encoded_image,"name":image_name,"label_txt":content,"label":label}
        collection.insert_one(document)
    data["message"].append("添加完毕")
    return data
def data_from_mongo(num_images_to_select):
    """
    从mongo中随机提取数据   
    """
    collection = mongo.db.image_data
    good_ids = get_all("good_id","goods")

    n =0 
    if os.listdir(image_flie_path):
        now_index = int(max(os.listdir(image_flie_path))[:-4]) +1 
    else:
        now_index = 0
    for good_id in good_ids:
        pipeline = {'label' :good_id}
        result = collection.find(pipeline)
        list_result = list(result)
        selected_images = random.sample(list_result, min(num_images_to_select, len(list_result)))
        for record in selected_images:
            image_data = base64.b64decode(record['image'])
            with open(image_flie_path +"/"+str(now_index)+".jpg", 'wb') as image_file:
                image_file.write(image_data)
            with open(label_flie_path +"/"+str(now_index)+".txt", 'wb') as label_file:
                label_file.write(record['label_txt'])
            now_index +=1 
        n +=len(selected_images)
    data = {}
    data["count"] = n
    return data
# def model_to_mongo():

