import os
import random
import yaml
import subprocess

from .get_good import get_cluster_centers,get_center_img,get_goods,resize_list,find_goods_centers,bg_around
from .convert import  convert_annotation,convert_data
from .lock import acquire_lock,release_lock
from instance.yolo_config import path_config,train_config
# xml解析包
sets = ['train', 'test', 'val']
classes = ['fall','candy'] # 标签值
imgfilepath = path_config['image_path']

labelfilpath = path_config['label_path']
trainval_percent = train_config["trainval_percent"]
train_percent = train_config["train_percent"]
yaml_path = path_config["yaml_path"]

lock_file_path = "lock_file.lock"
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
        name = imgfilepath +"/"+ total_img[i][:-4] +'.jpg'+ '\n'
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
def get_label_index(label):
    '''
    获取当前标签在yaml文件中的下标，若不存在，则加入
    '''
    # 读取 YAML 文件
    with open(yaml_path, 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    # 修改指定键的值
    if label in data['names']:
        return data['names'].index(label)
    else:
        data['names'].append(label)
        data['nc'] = len(data['names'])
        # 写入修改后的内容回到文件
        with open(yaml_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)
        return data['nc'] - 1 



def run_script(script_path):
    data = {}
    # 尝试获取文件锁
    lock_fd,lock_file = acquire_lock(script_path)
    if lock_fd is None:
        data["error"] = f"文件{script_path}已经在运行中，当前版本不支持重复运行"
        return data

    try:
        # 脚本的主要逻辑
        subprocess.run(['python', script_path])
        data["message"] = f"文件{script_path}开始运行"
    except :
        data["error"] = f"文件{script_path}在运行中出现问题"
    finally:
        # 释放文件锁
        release_lock(lock_fd,lock_file)
    return data


