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

    #--------------------------
    #直接通过判断聚类中心与背景的相似度即可
    # 越不像的越可能是商品位置
    #--------------------------
    n = len(cluster_center_img_list)
    # 寻找相似度最低的聚类中心
    match_list = [1]*n
    good_cluster_list = [None] *n
    bg_resize_img = cv2.resize(bg, (img_part_size*2,img_part_size*2))
    # 遍历图像
    for i in range(n):
        min_match = 1
        #遍历当前图像的所有聚类中心图像
        for index,cluster_center_img in enumerate(cluster_center_img_list[i]):
                # 提取当前图像的关键点和描述符
                similarity = ssim(bg_resize_img, cluster_center_img,channel_axis =2 )
                if  similarity <= min_match:
                    min_match = similarity
                    match_list[i] = index
        good_cluster_list[i] = cluster_center_img_list[i][match_list[i]]
    return match_list,good_cluster_list
def get_goods(bg_reisze_img,good_index_list,orign_resize_img_list,cluster_centers_list,cluster_border_list  ,size=img_size,is_show= False  ):
    '''
    根据获取到的商品聚类中心来寻找商品整体
    input :
        bg_reisze_img : 经过大小调整的背景图
        good_index_list : 商品的聚类中心下标
        orign_resize_img_list : 经过大小调整的原图列表
        cluster_centers_list : 图像聚类中心列表
        cluster_border_list : 图像聚类中心图像边界值
        size : 原图大小
        is_show : 是否显示二分过程
    output : 
        result : 保存所有商品边界值的列表
    '''
    result = []
    for index , i in enumerate(good_index_list):
        orign_resize_img = orign_resize_img_list[index]
        center_x,center_y = map(int,cluster_centers_list[index][i])
        left_x,right_x,left_y,right_y = cluster_border_list[index][i]
        left_x = binary (bg_reisze_img,orign_resize_img,(left_y,right_y) ,center_x,size=size,is_left =  False , is_x = True,is_show= is_show)
        right_x = binary (bg_reisze_img,orign_resize_img,(left_y,right_y) ,center_x,size=size,is_left = True ,is_x = True, is_show= is_show)
        if is_show: 
            cv2.imshow('1',orign_resize_img[:,left_x:right_x,:])
            cv2.waitKey(0)
        left_y = binary (bg_reisze_img,orign_resize_img,(left_x,right_x) ,center_y,size=size,is_left = False , is_x = False,is_show= is_show)
        right_y = binary (bg_reisze_img,orign_resize_img,(left_x,right_x) ,center_y,size=size,is_left = True, is_x = False,is_show= is_show)
        if is_show:
            print(index)
            cv2.imshow('test',orign_resize_img[left_y:right_y,left_x:right_x,:])
            cv2.waitKey(0)
        result.append((left_x,right_x,left_y,right_y))
    return result




    return result
def binary (bg_reisze_img,orign_resize_img,side ,site,size=img_size,is_left = False , is_x = True,is_show =False):
    """
    input :
        bg_reisze_img : 经过大小调整的背景图
        orign_resize_img : 经过大小调整的原图
        side : 当前二分轴的另一轴的最大最小值,默认为聚类中心裁剪图像的大小
        site : 聚类中心的坐标位置
        size : 图像大小
        is_left : 模式标志,当前所给site是否为left,left = site or 0 
        is_x : 模式标志,当前二分轴
        is_show: 是否展示二分过程
    output :
        left : 二分结果
    """
    if is_left :
        left = site 
        right = size[0] if is_x else size[1] 
    else:
        left = 0 
        right = site
    while left < right :
        mid = (left+right )//2 
        if right - mid  <= 7 :
            break
        if is_x :
            img_r =  orign_resize_img[side[0]:side[1],mid:right,:] if is_left else orign_resize_img[side[0]:side[1],left:mid,:]
            img_bg = bg_reisze_img[side[0]:side[1],mid:right,:] if is_left else bg_reisze_img[side[0]:side[1],left:mid,:] 
            if is_show:
                t1 = orign_resize_img.copy()
                t2 = orign_resize_img.copy()
                cv2.rectangle(t1, (mid, side[0]), (right, side[1]), (0, 255, 0), 2)
                cv2.rectangle(t2, (left, side[0]), (mid, side[1]), (0, 255, 0), 2)
        else:
            img_r = orign_resize_img[mid:right,side[0]:side[1],:] if is_left else orign_resize_img[left:mid,side[0]:side[1],:]
            img_bg = bg_reisze_img[mid:right,side[0]:side[1],:] if is_left else bg_reisze_img[left:mid,side[0]:side[1],:]
            if is_show:
                t1 = orign_resize_img.copy()
                t2 = orign_resize_img.copy()
                cv2.rectangle(t1, (side[0],mid), (side[1],right ), (0, 255, 0), 2)
                cv2.rectangle(t2, (side[0],left), (side[1],mid), (0, 255, 0), 2)

        similarity = ssim(img_r, img_bg,channel_axis =2)    
        if is_show:
            print(mid,right,side[0],side[1],is_x,is_left)
            cv2.imshow("l",t1)
            cv2.imshow("r",t2)
            cv2.imshow("img_r",img_r)
            cv2.imshow('img_bg',img_bg)
            cv2.waitKey(0)

            print(img_r.shape,similarity)
        if similarity > 0.90 :
            if is_left:
                right = mid 
            else:
                left = mid 
        else:
            if is_left:
                left = mid 
            else:
                right = mid 
    return left 
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