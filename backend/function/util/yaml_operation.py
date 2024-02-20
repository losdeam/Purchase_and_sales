
import yaml 
import os 
import shutil
from  .redis_operation import get_config_data
# from instance.yolo_config import path_config
# yaml_path = path_config['yaml_path']
def yaml_clear(yaml_path):
    '''
    清空yaml文件,若不存在则直接创建
    '''
    # 清空yaml中数据
    try :
        with open(yaml_path, 'r', encoding='utf-8') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
    except:
        with open(yaml_path, "w", encoding="utf-8") as f:
            yaml.dump({}, f)
        with open(yaml_path, 'r', encoding='utf-8') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)

    # 修改指定键的值
    data['names'] = []
    data['nc'] = 0
    data['test'] = "D:/code/Purchase_and_sales/backend/function/recognition/data/test.txt"
    data['train'] = 'D:/code/Purchase_and_sales/backend/function/recognition/data/train.txt'
    data['val'] = 'D:/code/Purchase_and_sales/backend/function/recognition/data/val.txt'
    # 写入修改后的内容回到文件
    with open(yaml_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)
    
def yaml_detele(yaml_path,label):
    if yaml_path == get_config_data('path_config','yaml_file_path') + "/goods0.yaml":
        os.remove(get_config_data('path_config','yaml_file_path') + "/goods1.yaml")
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
def yaml_create():
    '''
    以已有的最早的yaml文件作为范本进行新yaml文件的生成，若不存在yaml，则创建一个空的yaml
    '''
    yaml_file_path = get_config_data('path_config','yaml_file_path') 
    yaml_old = yaml_file_path +  "/goods1.yaml"
    yaml_new = yaml_file_path +  "/goods0.yaml"
    list_yaml_name =  os.listdir(yaml_file_path)

    if "goods1.yaml" in list_yaml_name:
        shutil.copy(yaml_old,yaml_new)
    else :
        yaml_clear(yaml_new)

    
def yaml_arrange():
    '''
    整理已有模型，维持队列的顺序
    '''
    yaml_file_path = get_config_data('path_config','yaml_file_path')
    list_yaml_name = os.listdir(yaml_file_path)
    used = set()
    def dfs(index,leak):
        if index > 5 or  index in used:
            return 
        old_model_path = yaml_file_path +  '/' +"goods" + str(index) +".yaml"
        new_model_path = yaml_file_path +  '/' +"goods" +str(index-leak+1) +".yaml"
        if old_model_path[-11:] in list_yaml_name:
            if new_model_path[-11:] in list_yaml_name and old_model_path!=new_model_path :
                dfs(index-leak+1,leak)
            if new_model_path == yaml_file_path + f'/goods{str(5+1)}.yaml' :
                os.remove(old_model_path)
                used.add(index)
                return 
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