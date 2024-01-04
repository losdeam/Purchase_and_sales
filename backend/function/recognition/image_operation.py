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
from .util import get_label_index,get_cluster_centers,get_center_img,get_goods,resize_list,convert_data,find_goods_centers
image_flie_path = path_config["image_path"]
label_flie_path = path_config["label_path"]
video_flie_path = path_config["video_path"]
target_frame_count = image_config['target_frame_count'] 
img_size = image_config['img_size']
goods_imgfile_path = path_config['goods_imgfile_path'] 
def count_time(f):
    def warrp(*a,**b):
        t1 = time.time()
        t = f(*a,**b)
        print(f.__name__,"耗时",time.time()-t1)
        return t
    return warrp


@count_time
def image_from_video( target_frame_count ,video=None ,output_folder = image_flie_path,video_flie_path=video_flie_path):
    '''
    从视频中获取图像数据，
    
    '''
    if  video:
        video_path = video_flie_path + '/' + '1.mp4'
        with open(video_path, 'wb') as f:
            f.write(video.read())
    
    video_dir = os.listdir(video_flie_path)

    output_list = []
    # print(video_dir)
    for index , video_name in  enumerate(video_dir):
        video_path = video_flie_path+"/"+video_name
        start_index = target_frame_count *  index
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        capture_interval = int(total_frames / target_frame_count)
        # 开始截取图像
        frame_count = 0
        while frame_count//capture_interval < target_frame_count:
            ret, frame = cap.read()
            if not ret:
                break  # 视频读取结束   
            # 每隔一定帧数截取一帧
            if frame_count % capture_interval == 0:
                output_path = os.path.join(output_folder, f"{start_index + frame_count // capture_interval}.jpg")
                output_list.append((frame,output_path))
            frame_count += 1
        # 释放视频捕捉对象
        cap.release()


    
    return output_list
@count_time
def image_read(img_list_withpath,label,bg_img,test= False):
    '''
    通过获取的图像列表,寻找商品所在位置，并截取对应位置生成对应的标签值
    imput:
        img_list_withpath: 带地址的图像列表（img,path)
        label: 图片的标签
        bg_img:背景图
    '''
    if not test:
        bg_img = cv2.imdecode(np.fromstring(bg_img.read(), np.uint8), cv2.IMREAD_COLOR)
    data = {}
    # 获取图像数据
    orign_resize_img_list,gray_resize_img_list,img_path_list= resize_list(img_list_withpath)
    for index,orign_resize_img in enumerate(orign_resize_img_list):
        cv2.imwrite(img_path_list[index],orign_resize_img)

    bg_reisze_img= cv2.resize(bg_img ,img_size)


    # 获取商品图片  
    cluster_center_img_list = []
    cluster_border_list =[]
    cluster_center_list = []
    for orign_resize_img in orign_resize_img_list:
        # 寻找聚类中心
        cluster_centers = get_cluster_centers(orign_resize_img)
        # 获取聚类中心图像
        cluster_center_img,cluster_border = get_center_img(orign_resize_img,cluster_centers)
        cluster_center_img_list.append(cluster_center_img)
        cluster_border_list.append(cluster_border)
        cluster_center_list.append(cluster_centers)

    goods_index_list,good_cluster_list = find_goods_centers(bg_reisze_img,cluster_center_img_list)
    goods_border = get_goods(bg_reisze_img,goods_index_list,orign_resize_img_list,cluster_center_list,cluster_border_list,is_show=False )



    # 生成yolo格式的标注数据
    for index,i in enumerate(goods_index_list):
        x_min,x_max,y_min,y_max = goods_border[index]
        good_img_path  = goods_imgfile_path + '/' + f"{index}" + ".jpg"
        cv2.imwrite(good_img_path,orign_resize_img_list[index][y_min:y_max,x_min:x_max])
        bb = convert_data(img_size,(x_min,x_max,y_min,y_max))
        with open(label_flie_path + "/"+f"{index}" + ".txt", 'w') as label_file:
            label_file.write(str(get_label_index(label)) + " " + " ".join([str(a) for a in bb]) + '\n')
    return data
