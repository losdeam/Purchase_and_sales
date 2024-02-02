

import random
import os 
import base64
import shutil
import cv2 
import numpy as np
import time 

# from instance.yolo_config import path_config,data_config
from flaskr.extensions import mongo
from .redis_operation import get_config_data
# from function.sql import get_all

# image_flie_path = path_config["image_file_path"]
# label_flie_path = path_config["label_file_path"]
# video_flie_path = path_config["video_file_path"]
# goods_imgfile_path = path_config['goods_imgfile_path'] 
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

def img_clear(user_id = 0):
    image_delete_local(get_config_data('path_config','image_file_path'))
    image_delete_local(get_config_data('path_config','label_file_path'))
    image_delete_local(get_config_data('path_config','goods_imgfile_path'))
    return "已清空图像与标签文件"