import pandas as pd 
import datetime 
import json
from collections import defaultdict
from flaskr.extensions import redis_client
from function.util import get_data,data_from_mongo,data_to_mongo
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from efficient_apriori import apriori
import copy 
def nonlinear_model(x, a, b):
    return a * x + b 
def test_add_data():
    '''
    仅供测试时使用，添加销售记录用于数据分析
    '''
    goods_id_list = redis_client.hkeys('goods_data')
    temp = {}

    for day in range(7):
        for goods_id in goods_id_list:
            goods_id = int(goods_id)
            nums = 50 -day*(goods_id % 3 - 1 )*3
            temp[goods_id] = nums
        message,flag = data_to_mongo("sales_records",{'time_stamp' : datetime.datetime.now()+datetime.timedelta(days=day),\
                                    'records_data' : temp
        })
    # print(message,flag )

def read_data():
    '''
    读取销售记录列表，并移除已下架商品
    '''
    data_result = []
    datas = data_from_mongo('sales_records')
    record_list = []
    if datas:
        for data in datas:
            temp = []
            goods_data = json.loads(data['records_data'])
            for id, num in goods_data.items():
                if redis_client.hget('goods_data', id): # 如果尚未下架，则显示销售记录

                    goods_name = get_data("goods_data",id)['name']
                    data_result.append({"time_stamp":data['time_stamp'],\
                                            "goods_id":id, \
                                            "goods_name":  goods_name,\
                                            "goods_num":num, \
                                            "goods_category" : get_data("goods_data",id)['category'],\
                                            "goods_reword" : (get_data("goods_data",id)['price_retail'] - get_data("goods_data",id)['price_buying']) * num
                                            })
                    temp.append(goods_name)
            if temp :
                record_list.append(temp)
            
            # print(data_result)
    return pd.DataFrame(data_result),record_list
def read_data_recent(df,n=3):
    df_copy = copy.copy(df)
    time_now = datetime.datetime.now()
    for x in df.index:
        sell_time = df_copy.loc[x, "time_stamp"]
        dis_time =  time_now-sell_time
        if dis_time.days >= n :
            df_copy.drop(x,inplace = True )
    return  df_copy 
def get_recent(df):
    '''
    获取近日最热门商品,销售额最高商品，各类中最热门商品，各类中销售额最高商品
    '''
    df_copy = read_data_recent(df)

    # 每种商品的销售总额
    total_sales_per_product = df_copy.groupby('goods_name')['goods_reword'].sum()
    # 每类商品的最高销量
    max_sales_per_category = df_copy.groupby(['goods_category', 'goods_id'])['goods_reword'].sum().groupby('goods_category').max()
    
    per_category = defaultdict(dict)
    for category_name,category_df in df_copy.groupby(['goods_category','goods_name'])['goods_reword'].sum().groupby('goods_category'):
        for  i,j in category_df.to_dict().items():
            per_category[category_name][i[1]] = j
    
    return total_sales_per_product.to_dict(),max_sales_per_category.to_dict(),per_category

def get_predict(df):
    '''
    计时，以n天为界限进行统计。构建预测模型
    '''
    result  = defaultdict(list)
    df_copy = read_data_recent(df)
    try:
        group_df = df_copy.groupby('goods_name')
        for name in group_df:
            x = np.array(list(map(lambda x: x.days,name[1]["time_stamp"] - datetime.datetime.now())) )
            y = np.array(name[1]["goods_reword"])
            model = LinearRegression()
            model.fit(x.reshape(-1, 1), y)
            # 绘制原始数据和拟合曲线
            new_x = np.array([6, 7, 8,9,10,11,12,13])
            y_pred = model.predict(new_x.reshape(-1, 1))
            result[name[0]] = list(y_pred)
    except:
        pass 
    return result

def get_apriori(record_list):
    print(record_list)
    itemsets ,rules = apriori(record_list,min_support=0.5,min_confidence=1)
    record = []
    print(itemsets ,rules)
    for i in rules:
        record.append([i.lhs,i.rhs])
    return record