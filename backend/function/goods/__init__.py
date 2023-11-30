from function.sql import upload_data,get_value, get_values
from flaskr.extensions import redis_client
from flask import jsonify
import datetime  

first_flag = True 
good_data = {}
def good_add(good_name ,good_num,good_price_buying,good_price_retail,good_sort,good_baseline):
    '''
    将good_id的商品的数量添加nums\n
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
    if not get_values(good_name,"good_name","goods"):
        upload_data({"good_name":good_name,"good_num":good_num,"good_price_buying":good_price_buying,"good_price_retail":good_price_retail,"good_sort":good_sort,"good_baseline":good_baseline},"goods")
        data = get_value(good_name,"good_name","goods")
        redis_client.hset("goods_num",data.good_id,good_num)
        redis_client.hset("goods_name",data.good_id,good_name)
        return jsonify(f"全新商品{good_name},编号为{data.good_id},数据添加成功,现库存量{good_num}")
    data = get_value(good_name,"good_name","goods")
    return jsonify(f"已存在同名商品{good_name},编号为{data.good_id}，商品添加失败")

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
    global first_flag 
    global good_data
    data_result = {}
    data_result["message"] = []
    goods_id_list = redis_client.hkeys('goods_name')
    for good_id in goods_id_list:
        good_id = int(good_id)
        if first_flag: # 第一次从数据库中读取，以获取变化频率较小的字段。
            data = get_value(good_id,"good_id","goods")
            good_data[good_id]= {
                "good_name" : data.good_name,
                "good_price_buying" : data.good_price_buying,
                "good_price_retail" : data.good_price_retail,
                "good_sort" : data.good_sort ,
                "good_baseline" : data.good_baseline
            }
        good_num = int(redis_client.hget('goods_num', good_id)) # 变化频率高的使用redis进行读取
        if good_num < good_data[good_id]["good_baseline"]:
            data_result["message"].append({"good_id":int(good_id),\
                                       "good_name":good_data[good_id]["good_name"], \
                                       "good_num":good_num, \
                                        "good_sort" : good_data[good_id]["good_sort"] , \
                                        "good_baseline" : good_data[good_id]["good_baseline"]\
                                       })
    first_flag = False  #使用一个global的变量来实现同一个用户只执行一次的操作
    return jsonify(data_result)


def good_show():
    '''
    展示所有商品及其库存
    '''
    global first_flag 
    global good_data
    data_result = {}
    data_result["message"] = []
    goods_id_list = redis_client.hkeys('goods_name')
    for good_id in goods_id_list:
        good_id = int(good_id)
        if first_flag: # 第一次从数据库中读取，以获取变化频率较小的字段。
            data = get_value(good_id,"good_id","goods")
            good_data[good_id]= {
                "good_name" : data.good_name,
                "good_price_buying" : data.good_price_buying,
                "good_price_retail" : data.good_price_retail,
                "good_sort" : data.good_sort ,
                "good_baseline" : data.good_baseline
            }
        good_num = int(redis_client.hget('goods_num', good_id)) # 变化频率高的使用redis进行读取
        data_result["message"].append({"good_id":int(good_id),\
                                       "good_name":good_data[good_id]["good_name"], \
                                       "good_price_buying":good_data[good_id]["good_price_buying"], \
                                       "good_num":good_num, \
                                       "good_price_retail" : good_data[good_id]["good_price_retail"], \
                                        "good_sort" : good_data[good_id]["good_sort"] , \
                                        "good_baseline" : good_data[good_id]["good_baseline"]\
                                       })
    first_flag = False  #使用一个global的变量来实现同一个用户只执行一次的操作
    return jsonify(data_result)

