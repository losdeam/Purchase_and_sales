from function.sql import upload_data,get_value, get_values
from flaskr.extensions import redis_client
from flask import jsonify
import json
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
        None : 直接对数据库进行操作\n
    '''
    redis_client.hincrby('goods_num', good_id, -nums)
    nums_now = int(redis_client.hget('goods_num', good_id))
    good_name = redis_client.hget('goods_name', good_id).decode('utf-8')
    msg = []
    if good_nums_verify(good_id,nums_now):
        msg.append(f"{good_id}号商品{good_name},商品数量过低")

    msg.append(f"{good_id}号商品{good_name},成功售出{nums}件物品，现库存量为{nums_now}")
    return msg

def good_nums_verify(good_id,nums):
    '''
    检验good_id的数量是否过少\n
    input:\n
        good_id : 商品id\n
        nums : 该商品现存总数\n
    output:\n
        Flag : 
            True : 提示管理员需要进行补货\n
            False : 不进行操作\n
    '''
    
    data = get_value(good_id,"good_id","goods")

    if data.good_baseline > 2 * nums :
        return  True 
    return False 

def good_show():
    '''
    展示所有商品及其库存
    '''
    data_result = {}
    data_result["message"] = []
    goods_id_list = redis_client.hkeys('goods_name')
    for good_id in goods_id_list:
        good_name = redis_client.hget('goods_name', good_id).decode('utf-8')
        good_num = int(redis_client.hget('goods_num', good_id))
        good_id = int(good_id)
        data_result["message"].append({"good_id":good_id,"good_name":good_name,"good_num":good_num})
    return jsonify(data_result)