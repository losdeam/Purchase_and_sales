import os
import random
import cv2 

from .get_good import get_cluster_centers,get_center_img,find_goods,resize_list
from .convert import  convert_annotation
from instance.yolo_config import path_config,trian_config
# xml解析包
sets = ['train', 'test', 'val']
classes = ['fall'] # 标签值
imgfilepath = path_config['image_path']
xmlfilepath = path_config['xml_path']
lablefilpath = path_config['lable_path']
trainval_percent = trian_config["trainval_percent"]
train_percent = trian_config["train_percent"]

def SplitDataset():
    '''
    训练、测试与验证集分割（在每一重新获取数据后都需要重新运行）
    '''
    total_img = os.listdir(imgfilepath)
    num = len(total_img)
    list = range(num)
    tv = int(num * trainval_percent)
    tr = int(tv * train_percent)
    trainval = random.sample(list, tv)
    train = random.sample(trainval, tr)

    ftrainval = open('function/recognition/data/trainval.txt', 'w')
    ftest = open('function/recognition/data/test.txt', 'w')
    ftrain = open('function/recognition/data/train.txt', 'w')
    fval = open('function/recognition/data/val.txt', 'w')

    for i in list:
        name = 'data/' + total_img[i][:-4] +'.jpg'+ '\n'
        if i in trainval:
            ftrainval.write(name)
            if i in train:
                ftrain.write(name)
            else:
                fval.write(name)
        else:
            ftest.write(name)

    ftrainval.close()
    ftrain.close()
    fval.close()
    ftest.close()



def tranform():
    '''
    对所有的文件数据集进行遍历
    做了两个工作：
　　　　１．将所有图片文件都遍历一遍，并且将其所有的全路径都写在对应的txt文件中去，方便定位
　　　　２．同时对所有的图片文件进行解析和转化，将其对应的bundingbox 以及类别的信息全部解析写到label 文件中去
    　　　　　最后再通过直接读取文件，就能找到对应的label 信息
    '''
    total_xml = os.listdir(imgfilepath)
    for file_name  in total_xml:
        image_id = file_name[:-4] 
        convert_annotation(image_id)

def image_read(label):
    '''
    读取img_file_path路径下的所有图片,寻找商品所在位置，并截取对应位置生成对应的标签值
    imput:
        label: 图片的标签
    '''
    img_name_list = os.listdir(imgfilepath)
    img_list = []
    for img_name in img_name_list:
        if img_name[-4:]  == ".jpg":
            img_path = imgfilepath + img_name
            img = cv2.imread(img_path)
            img_list.append(img)
    gray_resize_img_list= resize_list(img_list)
    cluster_center_img_list = []
    border_list = []
    for gray_resize_img in gray_resize_img_list:
        cluster_centers = get_cluster_centers(gray_resize_img)
        cluster_center_img,border = get_center_img(gray_resize_img,cluster_centers)
        
        cluster_center_img_list.append(cluster_center_img)
        border_list.append(border)

    good_index_list = find_goods(cluster_center_img_list)


    for index,i in enumerate(good_index_list):
        x_min,x_max,y_min,y_max = border_list[index][i]
        bb = convert((320,320),(x_min,x_max,y_min,y_max))
        with open(lablefilpath +img_name_list[index][:-4] + ".txt", 'w') as label_file:
            label_file.write(str(classes.index(label)) + " " + " ".join([str(a) for a in bb]) + '\n')

