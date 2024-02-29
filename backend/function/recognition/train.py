import os 
import time 
# from instance.yolo_config import path_config,data_config,model_config,data_config
from function.util import img_clear,image_from_mongo,image_to_mongo,image_delete_local
from .image_operation import image_from_video,image_read,get_newimg
from function.util import get_config_data,yaml_create,yaml_arrange
from .util import SplitDataset,run_script
import cv2 
import shutil
import ast
def count_time(f):
    def warrp(*a,**b):
        t1 = time.time()
        t = f(*a,**b)
        print(f.__name__,"耗时",time.time()-t1)
        return t
    return warrp
def get_data(video_flie_path,output_folder,img_size,target_frame_count,label,bg ,sample_size,bg_path,label_path,video=None):
    '''
    获取训练数据（视频数据+随机小批量原有数据）
    '''
    #先将文件夹中可能存在的图片与标注文件删除
    img_clear()
    #获取当前下标

    #从视频中获取数据
    img_list_withpath = image_from_video(video_flie_path,output_folder,target_frame_count,video)
    image_read(img_list_withpath,label,bg)


    get_newimg(output_folder,bg_path,label_path,img_size,sample_size*0.5)
    #从mongo中获取已存在标签的数据,
    image_from_mongo(sample_size)
    SplitDataset()
    return  "训练数据处理完毕"
def arrange_model():
    '''
    整理已有模型，维持队列的顺序
    '''
    list_model_name = os.listdir(get_config_data('path_config','model_file_path'))
    used = set()
    def dfs(index,leak):
        if index > 5 or  index in used:
            return 
        old_model_path = get_config_data('path_config','model_file_path') +  '/' +"best" + str(index) +".pt"
        new_model_path = get_config_data('path_config','model_file_path') +  '/' +"best" +str(index-leak+1) +".pt"

        if old_model_path[-8:] in list_model_name:
            if new_model_path[-8:] in list_model_name and old_model_path!=new_model_path :
                dfs(index-leak+1,leak)
            if new_model_path == get_config_data('path_config','model_file_path') + f'/best{str(5+1)}.pt' :
                os.remove(old_model_path)
                used.add(index)
                return 

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
    model_path = get_config_data('path_config','train_model_path') + '/' + "train"+"/" +'weights'+'/'+'best.pt'
    try:
        os.rename(model_path,get_config_data('path_config','model_file_path') + '/best0.pt')
    except :
        return "模型移动失败，检测是否是训练中断或者报错",0 
    return "模型移动成功",1 
@count_time
def train_new_label(label,bg,video=None):
    data = {'message':[],'error':[],'code':200}
    #-------------------- 数据获取 --------------------------
    train_model_path = get_config_data('path_config','train_model_path')
    video_flie_path = get_config_data('path_config','video_file_path')
    output_folder = get_config_data('path_config','image_file_path')
    target_frame_count = get_config_data('data_config','target_frame_count')
    sample_size = get_config_data('data_config','sample_size')
    img_size = ast.literal_eval(get_config_data('data_config','img_size'))
    bg_path = get_config_data('path_config','bg_imgfile_path')
    label_path = get_config_data('path_config','label_file_path')
    #--------------------清空之前的训练数据并获取训练数据--------------
    yaml_arrange()
    yaml_create()

    image_delete_local(train_model_path)

    message = get_data(video_flie_path,output_folder,img_size,target_frame_count,label,bg,sample_size,bg_path,label_path,video)
    data["message"].append(message) 
    # print(data)
    #---------------------------------------

    #--------------------训练模块--------------
    data_script = run_script()
    if 'message' in data_script:
        data["message"].append(data_script['message']) 
    if 'error' in data_script:
        data['error'].append(data_script['error']) 
        data['code'] = 403
        return  data
    # print(data)
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
    image_delete_local(get_config_data('path_config','train_model_path'))
    #先将文件夹中可能存在的图片与标注文件删除
    img_clear()
    #从mongo中获取已存在标签的数据,
    image_from_mongo(get_config_data('data_config','sample_size'))
    SplitDataset()
    #---------------------------------------

    #--------------------训练模块--------------
    # print(11123123,get_config_data('path_config','train_script_path'))
    data_script = (get_config_data('path_config','train_script_path'))
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