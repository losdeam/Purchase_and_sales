# from function.sql import upload_data,get_value, get_values,get_values_time,delete_value,update_data
from flaskr.extensions import redis_client
# from flaskr.models import Goods
from function.util import hash_password,verify_password,get_data,data_get_mongo,load_data,data_verify_total,yaml_read
from function.util import data_to_mongo ,data_from_mongo,data_update_mongo,data_delete_mongo,data_find_mongo
from function.util import image_delete_mongo,yaml_detele
from flask import jsonify
import pandas as pd 
import datetime  
import json

def data_get(goods_id):
    '''
    获取json数据
    '''
    data = redis_client.hget('goods_data', goods_id)
    return json.loads(data)
def goods_add(goods_name ,goods_num,goods_price_buying,goods_price_retail,goods_category,goods_baseline):
    '''
    添加全新商品s\n
    input:\n
        goods_name :商品id\n
        goods_num : 收入仓库的商品数量\n
        goods_price_buying : 商品的进货价\n
        goods_price_retail : 商品的零售价\n
        goods_category : 商品的类别\n
        goods_baseline : 商品的标准数量\n
    output:\n
        None : 直接对数据库进行操作\n
    '''
    data_result = {}
    data_result["message"] = ""
    data_result["code"] = 200
    if not data_find_mongo("goods_data","name",goods_name):
        data = {"name":goods_name,\
                "num":goods_num,\
                "price_buying":goods_price_buying,\
                "price_retail":goods_price_retail,\
                "category":goods_category,\
                "baseline":goods_baseline}
        print(data)
        message ,flag = data_to_mongo("goods_data",{"name":goods_name,\
                                                    "num":goods_num,\
                                                    "price_buying":goods_price_buying,\
                                                    "price_retail":goods_price_retail,\
                                                    "category":goods_category,\
                                                    "baseline":goods_baseline})
        if not flag :
            data_result["message"] = message
            return data_result
        data_id = data_get_mongo("goods_data",'id',{'name':goods_name})
        goods_data_json = json.dumps(data)
        redis_client.hset("goods_data",data_id,goods_data_json)
        redis_client.hset("goods_num",data_id,goods_num)
        data_result["message"] = f"全新商品{goods_name},编号为{data_id},数据添加成功,现库存量{goods_num}"
        data_result["goods_id"] = data_id
        
        return data_result
    data_id = data_get_mongo("goods_data",'id',{'name':goods_name})
    data_result["message"] = f"已存在同名商品{goods_name},编号为{data_id}，商品添加失败"
    data_result["code"] = 401

    return data_result
def goods_Replenish(goods_id,nums):
    '''
    将goods_id的商品的数量添加nums\n
    input:\n
        goods_id :商品id\n
        nums : 收入仓库的商品数量\n
    output:\n
        msg : 信息\n
    '''
    redis_client.hincrby('goods_num', goods_id, nums)
    nums_now = int(redis_client.hget('goods_num', goods_id))
    goods_name = json.loads(redis_client.hget('goods_data', goods_id))['name']
    return f"成功为{goods_id}号商品{goods_name},添加{nums}件物品，现库存量为{ nums_now}"
def goods_sell(goods_id,nums):
    '''
    将goods_id的商品的数量减去nums\n
    input:\n
        goods_id : 商品id\n
        nums : 卖出的商品数量\n
    output:\n
        msg : 信息\n
    '''
    if not redis_client.hget('goods_num', goods_id):
        return  jsonify(f"商品不存在或是已经下架") 
    nums_now = int(redis_client.hget('goods_num', goods_id))
    if nums > nums_now:
        return  jsonify(f"购买数量超过库存总量:{nums_now}，购买失效") 
    redis_client.hincrby('goods_num', goods_id, -nums)
    nums_now = int(redis_client.hget('goods_num', goods_id))
    goods_data = json.loads(redis_client.hget('goods_data', goods_id))
    msg = []
    
    msg.append(f"{goods_id}号商品{goods_data['name']},成功售出{nums}件物品，现库存量为{nums_now}")
    message,flag = data_to_mongo("sales_records",{'time_stamp' : datetime.datetime.now(),\
                                   'records_data' : {goods_id:nums}
    })
    return jsonify(msg)
def goods_nums_verify():
    '''
    检验goods_id的数量是否过少\n
    input:\n
    output:\n
        所有数量过低的商品
    '''
    data_result = {}
    data_result["message"] = []
    
    goods_id_list = redis_client.hkeys('goods_data')
    for goods_id in goods_id_list:
        
        goods_id = int(goods_id)
        goods_data = data_get(goods_id)
        goods_data["baseline"] = int(goods_data["baseline"])
        goods_num = int(redis_client.hget('goods_num', goods_id)) # 变化频率高的使用redis进行读取
        if goods_num <= goods_data["baseline"]:
            data_result["message"].append({"goods_id":int(goods_id),\
                                       "goods_name":goods_data["name"], \
                                       "goods_num":goods_num, \
                                        "goods_category" : goods_data["category"] , \
                                        "goods_baseline" : goods_data["baseline"]\
                                       })
    return jsonify(data_result)
def goods_show():
    '''
    展示所有商品及其库存
    '''
    data_result = {}
    data_result["message"] = []
    
    goods_id_list = redis_client.hkeys('goods_data')

    for goods_id in goods_id_list:
        
        goods_id = int(goods_id)
        goods_data = data_get(goods_id)
        goods_num = int(redis_client.hget('goods_num', goods_id)) # 变化频率高的使用redis进行读取
        data_result["message"].append({"goods_id":int(goods_id),\
                                       "goods_name":goods_data["name"], \
                                       "goods_price_buying":goods_data["price_buying"], \
                                       "goods_num":goods_num, \
                                       "goods_price_retail" : goods_data["price_retail"], \
                                        "goods_category" :goods_data["category"] , \
                                        "goods_baseline" : goods_data["baseline"]\
                                       })
    return jsonify(data_result)
def goods_delete(goods_id):
    '''
    删除对应的商品,带余量检测机制
    '''
    result = {}

    goods_num = int(redis_client.hget('goods_num', goods_id))
    goods_name = json.loads(redis_client.hget('goods_data', goods_id))['name']
    if goods_num != 0 :
        result["message"] = f"商品{goods_name}尚有库存{goods_num}件，无法删除"
        data = jsonify(result) 
        data.status_code = 401
        return data
    data_delete_mongo(goods_id,"id","goods_data")
    redis_client.hdel('goods_data', goods_id)
    redis_client.hdel('goods_num', goods_id)
    # image_delete_mongo(goods_id)

    # 需修改点： 加入商品标签在配置文件中的剔除
    # yaml_detele('./function/recognition/data/yaml/goods0.yaml',goods_id)

    result["message"] = f"{goods_id}号商品{goods_name},已成功删除"
    return jsonify(result) 
def goods_delete_f(goods_id):
    '''
    删除对应的商品，强制删除
    '''
    result = {}
    goods_name = json.loads(redis_client.hget('goods_data', goods_id))['name']
    data_delete_mongo(goods_id,"id","goods_data")
    
    redis_client.hdel('goods_data', goods_id)
    redis_client.hdel('goods_num', goods_id)
    result["message"] = f"{goods_id}号商品{goods_name},已成功删除"
    return jsonify(result) 
def goods_conifg(goods_id,new_data):
    '''
    更改商品的基本信息
    '''
    data_result = {}
    final_data = data_from_mongo('goods_data',{'id' :goods_id}) [0]
    for key,val in new_data.items():
        if val :
            final_data[key] = val
    data_result["message"] = data_update_mongo(goods_id,"goods_id","goods_data",final_data)
    json_final_data = json.dumps(final_data)
    redis_client.hset("goods_data",goods_id,json_final_data)
    result = jsonify(data_result)
    return result
def show_sale_record(n=3):
    '''
    展示销售记录
    input: 
        n : 调用次数，用于判断获取最近几天，默认为3
    '''
    data_result = {}
    data_result["message"] = []
    datas = data_from_mongo('sales_records')

    if datas:
        for data in datas:
            goods_data = json.loads(data['records_data'])
            for id, num in goods_data.items():
                data_result["message"].append({"time_stamp":str(data['time_stamp']),\
                                            "goods_id":id, \
                                            "goods_name": data_get(id)["name"] if redis_client.hget('goods_data', id) else "商品已下架",\
                                            "goods_num":num, \
                                            })
    result = jsonify(data_result)

    return result
