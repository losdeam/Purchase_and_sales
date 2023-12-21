from function.sql import upload_data,get_value, get_values,get_values_time,delete_value,update_data
from flaskr.extensions import redis_client
from flaskr.models import Goods
from flask import jsonify
import pandas as pd 
import datetime  
import string


good_data = {}
flag_init = True 

def data_init():
    '''
    页面数据初始化
    '''
    global good_data
    global flag_init 
    if flag_init:
        goods_list = Goods.query.all()
        for good in goods_list:
            good_id = good.good_id
            good_data[good_id]= {
                "good_name" : good.good_name,
                "good_price_buying" : good.good_price_buying,
                "good_price_retail" : good.good_price_retail,
                "good_sort" : good.good_sort ,
                "good_baseline" : good.good_baseline
            }
        flag_init = False
def good_add(good_name ,good_num,good_price_buying,good_price_retail,good_sort,good_baseline):
    '''
    添加全新商品s\n
    input:\n
        good_name :商品id\n
        good_num : 收入仓库的商品数量\n
        good_price_buying : 商品的进货价\n
        good_price_retail : 商品的零售价\n
        good_sort : 商品的类别\n
        good_baseline : 商品的标准数量\n
    output:\n
        None : 直接对数据库进行操作\n
    '''
    data_result = {}
    data_result["message"] = ""
    if not get_values(good_name,"good_name","goods"):
        upload_data({"good_name":good_name,"good_num":good_num,"good_price_buying":good_price_buying,"good_price_retail":good_price_retail,"good_sort":good_sort,"good_baseline":good_baseline},"goods")
        data = get_value(good_name,"good_name","goods")
        redis_client.hset("goods_num",data.good_id,good_num)
        redis_client.hset("goods_name",data.good_id,good_name)
        good_data[data.good_id]= {
                "good_name" : good_name,
                "good_price_buying" : good_price_buying,
                "good_price_retail" : good_price_retail,
                "good_sort" : good_sort ,
                "good_baseline" : good_baseline
            }
        data_result["message"] = f"全新商品{good_name},编号为{data.good_id},数据添加成功,现库存量{good_num}"
        data_result["good_id"] = data.good_id
        data_result["code"] = 200
        return data_result
    data = get_value(good_name,"good_name","goods")
    data_result["message"] = f"已存在同名商品{good_name},编号为{data.good_id}，商品添加失败"
    data_result["code"] = 403

    return data_result
def good_Replenish(good_id,nums):
    '''
    将good_id的商品的数量添加nums\n
    input:\n
        good_id :商品id\n
        nums : 收入仓库的商品数量\n
    output:\n
        msg : 信息\n
    '''
    redis_client.hincrby('goods_num', good_id, nums)
    nums_now = int(redis_client.hget('goods_num', good_id))
    good_name = redis_client.hget('goods_name', good_id).decode('utf-8')
    return f"成功为{good_id}号商品{good_name},添加{nums}件物品，现库存量为{ nums_now}"
def good_sell(good_id,nums):
    '''
    将good_id的商品的数量减去nums\n
    input:\n
        good_id : 商品id\n
        nums : 卖出的商品数量\n
    output:\n
        msg : 信息\n
    '''
    nums_now = int(redis_client.hget('goods_num', good_id))
    if nums > nums_now:
        return  jsonify(f"购买数量超过库存总量:{nums_now}，购买失效") 
    redis_client.hincrby('goods_num', good_id, -nums)
    nums_now = int(redis_client.hget('goods_num', good_id))
    good_name = redis_client.hget('goods_name', good_id).decode('utf-8')
    msg = []
    msg.append(f"{good_id}号商品{good_name},成功售出{nums}件物品，现库存量为{nums_now}")
    upload_data({"time_stamp":datetime.datetime.now(),"good_id":good_id,"good_num":nums},"sales_records")
    return jsonify(msg)
def good_nums_verify():
    '''
    检验good_id的数量是否过少\n
    input:\n
    output:\n
        所有数量过低的商品
    '''
    data_result = {}
    data_result["message"] = []
    data_init()
    goods_id_list = redis_client.hkeys('goods_name')
    for good_id in goods_id_list:
        good_id = int(good_id)
        good_num = int(redis_client.hget('goods_num', good_id)) # 变化频率高的使用redis进行读取
        if good_num <= good_data[good_id]["good_baseline"]:
            data_result["message"].append({"good_id":int(good_id),\
                                       "good_name":good_data[good_id]["good_name"], \
                                       "good_num":good_num, \
                                        "good_sort" : good_data[good_id]["good_sort"] , \
                                        "good_baseline" : good_data[good_id]["good_baseline"]\
                                       })
    return jsonify(data_result)
def good_show():
    '''
    展示所有商品及其库存
    '''

    data_result = {}
    data_result["message"] = []
    data_init()
    goods_id_list = redis_client.hkeys('goods_name')
    # print(good_data)
    for good_id in goods_id_list:
        good_id = int(good_id)
        good_num = int(redis_client.hget('goods_num', good_id)) # 变化频率高的使用redis进行读取
        data_result["message"].append({"good_id":int(good_id),\
                                       "good_name":good_data[good_id]["good_name"], \
                                       "good_price_buying":good_data[good_id]["good_price_buying"], \
                                       "good_num":good_num, \
                                       "good_price_retail" : good_data[good_id]["good_price_retail"], \
                                        "good_sort" : good_data[good_id]["good_sort"] , \
                                        "good_baseline" : good_data[good_id]["good_baseline"]\
                                       })
    return jsonify(data_result)
def good_delete(good_id):
    '''
    删除对应的商品
    '''
    result = {}
    data_init()
    good_num = int(redis_client.hget('goods_num', good_id))
    good_name = redis_client.hget('goods_name', good_id).decode()
    if good_num != 0 :
        result["message"] = f"商品{good_name}尚有库存{good_num}件，无法删除"
        data = jsonify(result) 
        data.status_code = 401
        return data
    delete_value(good_id,"good_id","goods")
    redis_client.hdel('goods_name', good_id)
    redis_client.hdel('goods_num', good_id)
    result["message"] = f"商品{good_name},已成功删除"
    return jsonify(result) 
def good_conifg(good_id,new_data):
    data_result = {}
    data_init()
    data_result["message"] = update_data(good_id,"good_id","goods",new_data)
    for key,value in new_data.items():
        if value :
            good_data[good_id][key] = value
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
    data_init()
    datas = get_values_time(datetime.datetime.now()- datetime.timedelta(days=n),"time_stamp","sales_records")
    if datas:
        for data in datas:
            data_result["message"].append({"time_stamp":data[0].time_stamp.strftime("%Y-%m-%d %H:%M:%S"),\
                                        "good_id":data[0].good_id, \
                                        "good_name": good_data[data[0].good_id]["good_name"] if data[0].good_id in good_data else "商品已下架",\
                                        "good_num":data[0].good_num, \
                                        })

    result = jsonify(data_result)

    return result
