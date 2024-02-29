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
def nonlinear_model(x, a, b):
    return a * x + b 
def test_add_data():
    '''
    仅供测试时使用，添加销售记录用于数据分析
    '''
    goods_id_list = redis_client.hkeys('goods_data')
    for goods_id in goods_id_list:
        for day in range(7):
            goods_id = int(goods_id)
            nums = 50 -day*(goods_id % 3 - 1 )*3
            message,flag = data_to_mongo("sales_records",{'time_stamp' : datetime.datetime.now()+datetime.timedelta(days=day),\
                                        'records_data' : {goods_id:nums}
            })
            print(message,flag )

def read_data():
    '''
    读取销售记录列表，并移除已下架商品
    '''
    data_result = []
    datas = data_from_mongo('sales_records')

    if datas:
        for data in datas:
            goods_data = json.loads(data['records_data'])
            for id, num in goods_data.items():
                if redis_client.hget('goods_data', id):
                    data_result.append({"time_stamp":data['time_stamp'],\
                                            "goods_id":id, \
                                            "goods_name": get_data("goods_data",id)['name'] ,\
                                            "goods_num":num, \
                                            "goods_category" : get_data("goods_data",id)['category'],\
                                            "goods_reword" : (get_data("goods_data",id)['price_retail'] - get_data("goods_data",id)['price_buying']) * num
                                            })
    return pd.DataFrame(data_result)
def read_data_recent(df,n=3):
    df_copy = df.copy()
    time_now = datetime.datetime.now()
    for x in df.index:
        sell_time = df_copy.loc[x, "time_stamp"]
        dis_time =  time_now-sell_time
        if dis_time.days >= n :
            df_copy.drop(x,inplace = True )
    return  df 
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
    result  = {}
    df_copy = read_data_recent(df)
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
    return result