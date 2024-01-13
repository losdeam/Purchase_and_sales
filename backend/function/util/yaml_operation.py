
import yaml 
from instance.yolo_config import path_config
yaml_path = path_config['yaml_path']
def yaml_clear(yaml_path):
    # 清空yaml中数据
    with open(yaml_path, 'r', encoding='utf-8') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    # 修改指定键的值
    data['names'] = []
    data['nc'] = 0
    # 写入修改后的内容回到文件
    with open(yaml_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)
    
def yaml_detele(yaml_path,label):
    # 清空yaml中数据
    with open(yaml_path, 'r', encoding='utf-8') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    # 修改指定键的值
    if label in data['names']:
        data['names'].remove(label)
        data['nc']-=1 
    # 写入修改后的内容回到文件
    with open(yaml_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

def yaml_get(yaml_path,label):
    with open(yaml_path, 'r', encoding='utf-8') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    if  label in data['names']:
        return True 
    return False 

def yaml_read(yaml_path):
    # 清空yaml中数据
    with open(yaml_path, 'r', encoding='utf-8') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    data = dict(data)
    # 写入修改后的内容回到文件
    return data 