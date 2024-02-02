
import yaml 
import os 
from  .redis_operation import get_config_data
# from instance.yolo_config import path_config
# yaml_path = path_config['yaml_path']
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
def yaml_arrange():
    '''
    整理已有模型，维持队列的顺序
    '''
    list_model_name = os.listdir(get_config_data('path_config','yaml_file_path'))
    used = set()
    def dfs(index,leak):
        if index > 5 or  index in used:
            return 
        old_model_path = get_config_data('path_config','yaml_file_path') +  '/' +"goods" + str(index) +".pt"
        new_model_path = get_config_data('path_config','yaml_file_path') +  '/' +"goods" +str(index-leak+1) +".pt"

        if old_model_path[-8:] in list_model_name:
            if new_model_path[-8:] in list_model_name and old_model_path!=new_model_path :
                    dfs(index-leak+1,leak)
            if new_model_path == get_config_data('path_config','model_file_path') + f'/goods{str(5+1)}.pt' :
                    os.remove(old_model_path)
                    used.add(index)
                    return 
            if new_model_path[-8:] in list_model_name and old_model_path!=new_model_path :
                dfs(index-leak+1,leak)
            os.rename(old_model_path,new_model_path)
            used.add(index)
        else:
            leak +=1 
        dfs(index+1,leak)
    dfs(0,0)    
def yaml_read(yaml_path):
    # 清空yaml中数据
    with open(yaml_path, 'r', encoding='utf-8') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    data = dict(data)
    # 写入修改后的内容回到文件
    return data 