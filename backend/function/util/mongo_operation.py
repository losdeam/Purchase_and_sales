
import random
import os 
import base64
import shutil
import cv2 
import numpy as np
from bson import json_util
import time 

# from instance.yolo_config import path_config,data_config
from flaskr.extensions import mongo,redis_client
# from function.sql import get_all
import json
from .model import image_model ,user_model,goods_model,Sales_records_model
from .redis_operation import get_config_data
def data_init():
    global collection_data
    collection_data = {
    "image" : mongo.db.image_data,
    "goods_data" : mongo.db.goods_data,
    "user_data" : mongo.db.user_data,
    "sales_records" : mongo.db.Sales_records
    }
    global collection_model
    collection_model = {
        "image" : image_model,
        "goods_data": goods_model,
        "user_data": user_model,
        "sales_records": Sales_records_model,
    }
    
    if not redis_client.exists('goods_data'):
        goods_data_list = data_from_mongo("goods_data")
        for goods_data in goods_data_list:
            goods_data_json = json.dumps(goods_data)
            redis_client.hset("goods_data",goods_data['id'],goods_data_json)
            redis_client.hset("goods_num",goods_data['id'],goods_data['num'])
    if not redis_client.exists('user_data'):
        user_data_list = data_from_mongo("user_data")
        for user_data in user_data_list:
            del user_data['password'] #不应该将密码保存至redis中，先行删去
            user_data_json = json.dumps(user_data)
            redis_client.hset("user_data",user_data['name'],user_data_json)
            
    return None 
def data_verify_type(type_,data):
    '''
    参数验证-格式验证
    '''
    model = collection_model[type_]
    # if len(model) != len(data):
    #     return False ,'参数数量有误'
    for argument in data:
        if argument not in model:
            return False,f"存在多余的参数{argument}"
        if not isinstance(data[argument] , model[argument]) and  not (type(data[argument]) in (float,int) and  model[argument] in (float,int) ):
            # print(type(data[argument]) in (float,int) , model[argument] in (float,int) )
            return False,f"{argument}参数格式错误,应为{model[argument]},实际为{type(data[argument])}"
        if isinstance(data[argument] , dict) :
            data[argument]  =  json.dumps(data[argument], default=json_util.default)

    return True,"参数格式验证通过"
def data_verify_unique(type_,data):
    '''
    参数验证-存在性验证
    '''
    model = collection_data[type_]

    if model.find_one({"name": {"$exists": True}}):
        # print({"name": data['name']})
        if  ('name' in data and model.find_one({"name": data['name']})) or \
            ('id' in data and model.find_one({"id": data['id']})):
            return False,f'已存在同名记录'
    return True,"参数存在性验证通过"
def data_verify_total(type_,data):
    '''
    参数验证-合集
    '''
    result = {}
    result['flag'] = True 
    result['message'] = []
    flag,message = data_verify_type(type_,data)
    result['flag']  = flag and result['flag']
    result['message'].append(message)
    flag,message = data_verify_unique(type_,data)
    result['flag']  = flag and result['flag']
    result['message'].append(message)
    return result

def image_delete_mongo(label):
    """
    删除mongo中数据
    """
    collection = mongo.db.image_data

    # 构建删除条件
    query = {"label": label}

    # 删除具有特定字段值的所有记录
    result = collection.delete_many(query)
    # 返回删除的记录数量
    return {'deleted_count': result.deleted_count}
def image_delete_mongo_all():
    """
    删除mongo中数据
    """
    collection = mongo.db.image_data
    # 删除具有特定字段值的所有记录
    result = collection.drop()
    # 返回删除的记录数量
    return {'message': "mongo中的数据清理完毕"}
def image_to_mongo(label):
    """
    将训练数据保存至mongo数据库中
    """
    data = {}
    data["message"] = []
    collection = mongo.db.image_data
    for image_name  in range(get_config_data('data_config','target_frame_count')):
        image_path_single =  get_config_data('path_config','image_file_path') +"/"+ str(image_name) + ".jpg"
        label_path_single = get_config_data('path_config','label_file_path') +"/"+ str(image_name) + ".txt"
        with open(image_path_single, 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read())
        with open(label_path_single, 'rb') as label_file:
            content = label_file.read()
        document = {'image':encoded_image,"label_txt":content,"label":label}
        collection.insert_one(document)
    data["message"].append("添加完毕")
    return data

def image_from_mongo(num_images_to_select):
    """
    从mongo中随机提取数据   
    """
    collection = mongo.db.image_data
    goods_ids = redis_client.hkeys('goods_data')
    image_flie_path = get_config_data('path_config','image_file_path')
    label_flie_path = get_config_data('path_config','label_file_path')
    n =0 
    if os.listdir(image_flie_path):
        now_index = int(max(os.listdir(image_flie_path))[:-4]) +1 
    else:
        now_index = 0
    for goods_id in goods_ids:
        goods_id_ = int(goods_id)
        pipeline = {'label' :goods_id_}
        result = collection.find(pipeline)
        list_result = list(result)  
        selected_images = random.sample(list_result, min(num_images_to_select, len(list_result)))
        # print(list_result,goods_id_,goods_ids)
        for record in selected_images:
            image_data = base64.b64decode(record['image'])
            with open(image_flie_path +"/"+str(now_index)+".jpg", 'wb') as image_file:
                image_file.write(image_data)
            with open(label_flie_path +"/"+str(now_index)+".txt", 'wb') as label_file:
                label_file.write(record['label_txt'])
            now_index +=1 
        n +=len(selected_images)
    data = {}
    data["count"] = n
    return data

def data_from_mongo(type_,pipe = {}):
    '''
    从mongo中获取type_的数据
    input:
        type_ : mongo表名
    output:
        result : 列表格式的数据
    '''
    projection = {"_id": 0}
    collection = collection_data[type_]
    result = collection.find(pipe,projection)
    return list(result)
def data_to_mongo(type_,data):
    '''
    将data写入mongo的type_表中
    input:
        type_ : mongo表名
        data : 数据
    output:
        message : 信息
    '''
    verify_result  = data_verify_total(type_,data)
    flag = verify_result['flag']
    message =  verify_result['message']
    
    if flag:
        try:
            collection = collection_data[type_]
            if collection.find_one({"id": {"$exists": True}}):
                max_id = collection.find().sort('id', -1).limit(1)[0]['id']
                data["id"] = max_id + 1 
            else:
                data["id"] =  1 
            collection.insert_one(data)
            del data["_id"]
            
            if type_ == "user_data":
                del data["password"]
                user_data_json = json.dumps(data, default=json_util.default)
                redis_client.hset(type_,data['name'],user_data_json)
            else :
                user_data_json = json.dumps(data, default=json_util.default)
                redis_client.hset(type_,data['id'],user_data_json)    
            return '添加完成',flag
        except Exception as e :
            # collection.delete_many({'name':data['name']})
            print(e)
    else :
        return message,flag
def data_find_mongo(type_,key,data):
    '''
    从mongo中的type_表查找key字段中是否存在data数据
    input:
        type_ : mongo表名
        key : 字段名
        data : 数据
    output:
        message : 信息
    '''
    collection = collection_data[type_]
    pipeline = {key :data}
    # 定义投影，排除 "_id" 字段
    projection = {"_id": 0}

    # 执行查询
    result = collection.find_one(pipeline, projection)

    return result 
def data_get_mongo(type_,key,pipe):
    '''
    读取mongo的type_表中的key字段
    input:
        type_ : mongo表名
        key : 键名
        pipe : 查询限制条件
    output:
        message : 信息
    '''
    projection = {"_id": 0}
    collection = collection_data[type_]
    result = list(collection.find(pipe,projection))
    return  result[0][key] if result else None 
def data_update_mongo(filter_data, filter_key, sheet,new_data):
    result = {}
    collection = collection_data[sheet]
    filter_criteria = {filter_key: filter_data }
    update_data = {'$set': new_data}

    collection.update_one(filter_criteria, update_data)
    # 更新单个文档
    return '更新成功'
def data_delete_mongo(data, key, sheet):
    """
    从sheet表中找到与key字段中与data相匹配的记录，并删除
    """
    collection = collection_data[sheet]
    # 构建删除条件
    query = {key: data}
    # 删除具有特定字段值的所有记录
    result = collection.delete_many(query)
    # 返回删除的记录数量
    return {'deleted_count': result.deleted_count}

