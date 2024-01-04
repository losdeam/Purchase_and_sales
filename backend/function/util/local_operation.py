

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
goods_imgfile_path = path_config['goods_imgfile_path'] 
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

def img_clear():
    image_delete_local(image_flie_path)
    image_delete_local(label_flie_path)
    image_delete_local(goods_imgfile_path)
    return "已清空图像与标签文件"