import random
import os 
import base64
import shutil
import cv2 
import numpy as np
import time 
import ast
from flaskr.extensions import mongo
from .util import get_label_index,get_cluster_centers,get_center_img,get_goods,resize_list,convert_data,find_goods_centers
from function.util import get_config_data
os.environ["OMP_NUM_THREADS"] = '1'
def count_time(f):
    def warrp(*a,**b):
        t1 = time.time()
        t = f(*a,**b)
        print(f.__name__,"耗时",time.time()-t1)
        return t
    return warrp
@count_time
def image_from_video( video_flie_path,output_folder,target_frame_count ,video=None ):
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
    goods_imgfile_path = get_config_data('path_config','goods_imgfile_path')
    img_size = get_config_data('data_config','img_size')
    img_size = ast.literal_eval(img_size)
    label_flie_path = get_config_data('path_config','label_file_path')

    img_size
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

    goods_index_list,goods_cluster_list = find_goods_centers(bg_reisze_img,cluster_center_img_list)
    goods_border = get_goods(bg_reisze_img,goods_index_list,orign_resize_img_list,cluster_center_list,cluster_border_list,is_show=False )



    # 生成yolo格式的标注数据
    for index,i in enumerate(goods_index_list):
        x_min,x_max,y_min,y_max = goods_border[index]
        goods_img_path  = goods_imgfile_path + '/' + f"{index}" + ".jpg"
        cv2.imwrite(goods_img_path,orign_resize_img_list[index][y_min:y_max,x_min:x_max])
        bb = convert_data(img_size,(x_min,x_max,y_min,y_max))
        with open(label_flie_path + "/"+f"{index}" + ".txt", 'w') as label_file:
            label_file.write(str(get_label_index(label)) + " " + " ".join([str(a) for a in bb]) + '\n')
    return data
@count_time
def get_newimg(origin_path,background_path,label_path,size,newbkimg_len):
    '''
    根据所给图像，在更换背景后生成全新的图像，以进行数据增强。(严格限制图像格式为JPG,标签格式为TXT)
    input:
        origin_path : 原图文件夹路径
        background_path : 背景图像位置(更换背景)
        label_path : 标签位置
        size : 图像调整后大小
        newbkimg_len : 与原图中采样进行背景更换的数量
    output:
        无
    '''
    # print(size )
    origin_path_list = os.listdir(origin_path)
    if origin_path_list:
        now_index = max(map(lambda x : int(x[:-4]),origin_path_list)) +1 
    else:
        now_index = 0
    sample_list = random.sample(origin_path_list, int(newbkimg_len))
    for name in sample_list:
        img_name = name[:-4]
        img_path = origin_path + "/" + img_name + '.jpg'
        foreground = cv2.imread(img_path)
        foreground = cv2.resize(foreground,size)
        gray = cv2.cvtColor(foreground,cv2.COLOR_BGR2GRAY)
        min_value=100
        ret, mask = cv2.threshold(gray, min_value, 255, cv2.THRESH_BINARY + cv2.THRESH_TRIANGLE)
        
        # 反转蒙版
        mask_inv = cv2.bitwise_not(mask)

        for i in os.listdir(background_path):
            label_origin_path = label_path +"/"+ img_name+'.txt'
            label_new_path = label_path +"/"+str(now_index)+'.txt'
            background = cv2.imread(background_path+"/"+i)
            background = cv2.resize(background,size)
            # 将前景和背景分别与蒙版相乘
            foreground_masked =cv2.bitwise_and(foreground, foreground, mask=mask_inv)
            background_masked = cv2.bitwise_and(background, background, mask=mask)
            # 合成图像
            result = cv2.add(foreground_masked, background_masked)
            cv2.imwrite(origin_path+"/"+str(now_index)+'.jpg',result)
            shutil.copy(label_origin_path,label_new_path)
            now_index+=1 


