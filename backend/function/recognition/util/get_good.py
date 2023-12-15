import cv2
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import mean_squared_error
from .convert import convert
from instance.yolo_config import image_config
img_part_size = image_config['img_part_size']
num_clusters = image_config['num_clusters']

# 使用 BRISK 特征检测器
brisk = cv2.BRISK_create()
bf = cv2.BFMatcher()
def get_cluster_centers(img):
    '''
    获取图像中关键点的聚类中心
    input:
        img:图像
        num_clusters : 返回的聚类中心的个数
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
        shape_x,shape_y = gray_img.shape
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
        cluster_centers_img = gray_img[x_min:x_max,y_min:y_max]
        cluster_centers_img_list.append(cluster_centers_img)
        border_list.append([x_min,x_max,y_min,y_max])
    return cluster_centers_img_list,border_list
def find_goods(cluster_center_img_list):
    '''
    寻找每张图的商品所在的聚类中心
    '''
    # 先通过一次遍历来寻找第一张图中商品的聚类中心
    result = []
    first_cluster_center= cluster_center_img_list[0]
    # 寻找相似度最高的聚类中心
    match_list = [0]*num_clusters
    # 遍历其他图像
    for i in range(1, len(cluster_center_img_list)):
        max_match_list = [0]*num_clusters
        for img_sec in cluster_center_img_list[i]:
            for index , img_first in  enumerate(first_cluster_center):
                # 提取当前图像的关键点和描述符
                similarity = mean_squared_error(img_sec, img_first)
                
                max_match_list[index] = max(max_match_list[index],similarity)
        for i in range(num_clusters):
            match_list[i] += max_match_list[i]
    good_center_index = match_list.index(max(match_list))
    good_center_img_first = first_cluster_center[good_center_index]

    result.append(good_center_index)

    for i in range(1, len(cluster_center_img_list)):
        max_match = 0
        good_center_img = None 
        for index,img_sec in enumerate(cluster_center_img_list[i]):
            similarity = mean_squared_error(img_sec, good_center_img_first)
            if max_match < similarity:
                max_match = similarity
                good_center_img = index
        result.append(good_center_img)
    return result
def resize_list(img_list):
    gray_result = []
    for img in img_list:
        img = cv2.resize(img,(320,320))
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray_result.append(gray_img)
    return gray_result





