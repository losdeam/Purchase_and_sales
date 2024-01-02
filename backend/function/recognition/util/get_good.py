import cv2
import numpy as np
from sklearn.cluster import KMeans

from skimage.metrics import structural_similarity as ssim
from instance.yolo_config import image_config,path_config
img_part_size = image_config['img_part_size']
num_clusters = image_config['num_clusters']
img_size = image_config['img_size']
cluster_centers_file = path_config['cluster_centers_filepath']

# 使用 BRISK 特征检测器
brisk = cv2.SIFT_create()
bf = cv2.BFMatcher()
def get_cluster_centers(img):
    '''
    获取图像中关键点的聚类中心
    input:
        img:图像
    output:
        cluster_centers: 聚类中心的坐标
    '''
    # 在图像上检测关键点
    keypoints, _ = brisk.detectAndCompute(img, None)
    keypoint_coordinates = np.array([kp.pt for kp in keypoints])
    kmeans = KMeans(n_clusters=num_clusters,n_init=10 ,random_state=42)
    kmeans.fit(keypoint_coordinates)
    # 获取聚类中心的坐标,
    cluster_centers = kmeans.cluster_centers_
    return cluster_centers
def get_center_img(gray_img,center_list):
    '''
    根据所给坐标在图像中截取一定大小的片段
    input:
        orign_img:原始图像
        center_list : 该图聚类中心的列表
        img_part_size:截取图像的大小(由聚类中心向四周延长的距离)
    output:
        cluster_centers: 聚类中心的坐标
    '''
    cluster_centers_img_list = []
    border_list = []
    for center_x,center_y in center_list:
        shape_x,shape_y,_ = gray_img.shape
        # 计算图像边界坐标
        x_min = int(center_x - img_part_size)  if center_x - img_part_size>= 0 else 0 
        x_max = int(center_x + img_part_size)  if center_x + img_part_size< shape_x else shape_x
        y_min = int(center_y - img_part_size)  if center_y - img_part_size>= 0 else 0 
        y_max = int(center_y + img_part_size)  if center_y + img_part_size< shape_y else shape_y 
        # 计算填充值
        extend_x = 2 * img_part_size - x_max + x_min
        extend_y = 2 * img_part_size - y_max + y_min
        if extend_x:
            if x_min :
                x_min -= extend_x
            else:
                x_max += extend_x

        if extend_y:
            if y_min :
                y_min -= extend_y
            else:
                y_max += extend_y
        
        # 根据图像边界坐标在原图中进行截图
        cluster_centers_img = gray_img[y_min:y_max,x_min:x_max]
        cluster_centers_img_list.append(cluster_centers_img)
        border_list.append([x_min,x_max,y_min,y_max])
    return cluster_centers_img_list,border_list
def find_goods_centers(bg,cluster_center_img_list):
    '''
    寻找每张图的商品所在的聚类中心
    '''
    # 先通过一次遍历来寻找第一张图中商品的聚类中心
    #--------------------------
    #直接通过判断聚类中心与背景的相似度即可
    # 越不像的越可能是商品位置
    #--------------------------
    n = len(cluster_center_img_list)
    # 寻找相似度最低的聚类中心
    match_list = [1]*n
    good_cluster_list = [None] *n
    # 遍历图像
    for i in range(n):
        min_match = 1
        #遍历当前图像的所有聚类中心图像
        for index,cluster_center_img in enumerate(cluster_center_img_list[i]):
                # 提取当前图像的关键点和描述符
                cluster_center_img_resize = cv2.resize(cluster_center_img, (320,320))

                similarity = ssim(bg, cluster_center_img_resize,channel_axis =2)
                if  similarity <= min_match:
                    min_match = similarity
                    match_list[i] = index
        good_cluster_list[i] = cluster_center_img_list[i][match_list[i]]
    return match_list,good_cluster_list
def get_goods(bg_reisze_img,good_index_list,orignimg_bg_around_list,border_list,size=img_size):
    '''
    根据获取到的商品聚类中心来寻找商品整体
    input:
        bg_reisze_img : 经过大小调整的背景图
        good_index_list : 获取到的聚类中心在对应图像聚类中心列表中的下标
        orignimg_bg_around_list : 被背景包围的原图，大小为(3*size,3*size)
        border_list : 图像聚类中心的边界列表
    output:
        result : 商品图像边界值列表
    '''
    result = []
    for index,i in enumerate(good_index_list):
        temp = [0] *4 
        good_border  = border_list[index][i]
        center_x ,center_y = good_border[0] + img_part_size ,good_border[2] +50
        # 当使用0,1,2,3的顺序时，若是聚类中心恰好在中心点时便会出现，两个x，两个y分成一组的情况，所以需要使用0,2,1,3的顺序避免
        distance = sorted([(good_border[0],0),(img_size[0]-good_border[1],2),(good_border[2],1),(img_size[1]-good_border[3],3) ])
        # print(distance)
        val1 = [distance[0],distance[1]]
        val2 = [distance[2],distance[3]]
        size1 = binary(val1,bg_reisze_img,orignimg_bg_around_list[index],center_x ,center_y)
        size2 = binary(val2,bg_reisze_img,orignimg_bg_around_list[index],center_x ,center_y)
        for i in range(4):
            if size1[i] != -1 :
                temp[i] = size1[i]
            else:
                temp[i] = size2[i]  
        result.append(temp)
    return result 
def binary (val,bg_reisze_img,orignimg_bg_around,center_x ,center_y):
    '''
    二分算法部分，通过二分算法来寻找恰当的尺寸
    '''
    left = img_part_size
    right = val[0][0] + img_part_size
    
    if val[0][1] == 0 :
        x_way_l = -1
        x_way_r = 0
    elif val[0][1] == 2 :
        x_way_l = 0
        x_way_r = 1
    elif val[0][1] == 1 :
        y_way_l = -1 
        y_way_r = 0
    else:
        y_way_l = 0 
        y_way_r = 1

    if val[1][1] == 0 :
        x_way_l = -1
        x_way_r = 0
    elif val[1][1] == 2 :
        x_way_l = 0
        x_way_r = 1
    elif val[1][1] == 1 :
        y_way_l = -1 
        y_way_r = 0
    else:
        y_way_l = 0 
        y_way_r = 1
    
    def get_data(size_part,x_way_l,y_way_l):
        x_min = x_max = y_min = y_max = -1 
        if x_way_l:
            x_min = center_x - size_part  if center_x >= size_part else  0 
        else:
            x_max = center_x + size_part  if center_x+size_part <  img_size[0] else  img_size[0] 
        if y_way_l:
            y_min = center_y - size_part  if center_y >= size_part else  0 
        else:
            y_max = center_y + size_part  if center_y+size_part <  img_size[1] else  img_size[1]
        return x_min, x_max , y_min , y_max

    while left<right:
        mid = (left+right) //2 
        # 截取二分区域图像(存在重复运算，后期可优化)
        img_l = orignimg_bg_around[center_y+img_size[0]+y_way_l*left: center_y+img_size[0]+y_way_r*left,center_x+img_size[0]+x_way_l*left: center_x+img_size[0]+x_way_r*left,:]
        img_mid = orignimg_bg_around[center_y+img_size[0]+y_way_l*mid: center_y+img_size[0]+y_way_r*mid,center_x+img_size[0]+x_way_l*mid: center_x+img_size[0]+x_way_r*mid,:]
        img_right = orignimg_bg_around[center_y+img_size[0]+y_way_l*right: center_y+img_size[0]+y_way_r*right,center_x+img_size[0]+x_way_l*right: center_x+img_size[0]+x_way_r*right,:]
        # 将二分图像整合为相同大小
        img_l_resize  = cv2.resize(img_l,img_size)
        img_mid_resize  = cv2.resize(img_mid,img_size)
        img_right_resize  = cv2.resize(img_right,img_size)

        # 获取二分区域图像与背景图的相似度
        similarity_left = ssim(bg_reisze_img, img_l_resize,channel_axis =2)
        similarity_mid = ssim(bg_reisze_img, img_mid_resize,channel_axis =2)
        similarity_right = ssim(bg_reisze_img, img_right_resize,channel_axis =2)
        if similarity_right < similarity_left and similarity_right < similarity_mid:
            return get_data(right,x_way_l,y_way_l)
        if similarity_left < similarity_right and similarity_left < similarity_mid:
            return get_data(left,x_way_l,y_way_l)
        if similarity_mid < similarity_right : 
            right = mid -1 
        else:
            left = mid +1 
    return get_data(right,x_way_l,y_way_l)
def resize_list(img_list):
    '''
    '''
    result= []
    gray_result = []
    img_path_list =[]
    for img,path in img_list:
        
        img = cv2.resize(img,img_size)
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        result.append(img)
        gray_result.append(gray_img)
        img_path_list.append(path)
    return result,gray_result,img_path_list
def bg_around(bg_reisze_img,orign_resize_img_list):
    '''
    用背景图将原始图像包围,以防止越界的产生
    '''
    result =[]
    for orign_resize_img in orign_resize_img_list:
        result_horizontal1 = np.concatenate((bg_reisze_img, bg_reisze_img,bg_reisze_img), axis=1)
        result_horizontal2 = np.concatenate((bg_reisze_img, orign_resize_img,bg_reisze_img), axis=1)
        result_horizontal3 = np.concatenate((bg_reisze_img, bg_reisze_img,bg_reisze_img), axis=1)
        result_vertical = np.concatenate((result_horizontal1,result_horizontal2,result_horizontal3), axis=0)
        result.append(result_vertical)
    return result