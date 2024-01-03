import os 
import time 
from instance.yolo_config import path_config,train_config,image_config,model_config
from .image_operation import image_from_video,img_clear,image_read,data_from_mongo,image_to_mongo,image_delete_local
from .util import SplitDataset,run_script


use_model_path = path_config['model_path']
image_flie_path = path_config["image_path"]
video_flie_path = path_config["video_path"]
num_images_to_select = train_config['sample_size']
target_frame_count = image_config['target_frame_count'] # 从视频中获取的图像数量
train_model_path = path_config['train_model_path'] 
train_script_path = path_config['train_script_path'] 
model_file_path = path_config['model_file_path'] 
model_max_len = model_config["max_len"] 
def count_time(f):
    def warrp(*a,**b):
        t1 = time.time()
        t = f(*a,**b)
        print(f.__name__,"耗时",time.time()-t1)
        return t
    return warrp
def get_data(label,bg , video=None):
    '''
    获取训练数据（视频数据+随机小批量原有数据）
    '''
    #先将文件夹中可能存在的图片与标注文件删除
    img_clear()
    #获取当前下标

    #从视频中获取数据
    img_list_withpath = image_from_video(target_frame_count,video)
    image_read(img_list_withpath,label,bg)
    #从mongo中获取已存在标签的数据,
    data_from_mongo(num_images_to_select)
    SplitDataset()
    return  "训练数据处理完毕"
def arrange_model():
    '''
    整理已有模型，维持队列的顺序
    '''
    list_model_name = os.listdir(model_file_path)
    used = set()
    def dfs(index,leak):
        if index > model_max_len or  index in used:
            return 
        old_model_path = model_file_path +  '/' +"best" + str(index) +".pt"
        new_model_path = model_file_path +  '/' +"best" +str(index-leak+1) +".pt"

        if old_model_path[-8:] in list_model_name:
            if new_model_path[-8:] in list_model_name and old_model_path!=new_model_path :
                    dfs(index-leak+1,leak)
            if new_model_path == model_file_path + f'/best{str(model_max_len+1)}.pt' :
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
def move_ptomodel():
    """
    将训练好的模型转移至模型文件夹中
    1. 保存原有模型
    2. 覆盖原有模型
    """
    arrange_model()
    model_path = train_model_path + '/' + "train"+"/" +'weights'+'/'+'best.pt'
    try:
        os.rename(model_path,model_file_path + '/best0.pt')
    except :
        return "模型移动失败，检测是否是训练中断或者报错",0 
    return "模型移动成功",1 
@count_time
def train_new_label(label,bg,video=None):
    data = {'message':[],'error':[],'code':200}
    #--------------------清空之前的训练数据并获取训练数据--------------
    image_delete_local(train_model_path)
    message = get_data(label,bg,video)
    data["message"].append(message) 
    #---------------------------------------

    #--------------------训练模块--------------
    data_script = run_script(train_script_path)
    if 'message' in data_script:
        data["message"].append(data_script['message']) 
    if 'error' in data_script:
        data['error'].append(data_script['error']) 
        data['code'] = 403
        return  data
    #---------------------------------------
        
    #--------------------数据保存--------------
    image_to_mongo(label)
    #--------------------------------------

    #--------------------将新模型保存到对应路径--------------
    message,flag = move_ptomodel()
    if flag :
        data["message"].append(message)
    else:
        data['error'].append(message)
        data['code'] = 404
        return  data
    #--------------------------------------
    
    return data

def train_strengthen():
    data = {'message':[],'error':[],'code':200}
    #--------------------清空之前的训练数据并获取训练数据--------------
    image_delete_local(train_model_path)
    #先将文件夹中可能存在的图片与标注文件删除
    img_clear()
    #从mongo中获取已存在标签的数据,
    data_from_mongo(num_images_to_select)
    SplitDataset()
    #---------------------------------------

    #--------------------训练模块--------------
    data_script = run_script(train_script_path)
    if 'message' in data_script:
        data["message"].append(data_script['message']) 
    if 'error' in data_script:
        data['error'].append(data_script['error']) 
        data['code'] = 403
        return  data
    #---------------------------------------

    #--------------------将新模型保存到对应路径--------------
    message,flag = move_ptomodel()
    if flag :
        data["message"].append(message)
    else:
        data['error'].append(message)
        data['code'] = 404
        return  data
    #--------------------------------------
    
    return data
     
    # 
if __name__ == "__main__":
    print("训练开始")

    # train_new_label()
    # train_new_label()
    print("训练结束")