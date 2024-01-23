import pandas as pd 
import datetime 
import json
from collections import defaultdict
from flaskr.extensions import redis_client
from function.util import get_data,data_from_mongo
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
                                            "goods_sort" : get_data("goods_data",id)['sort'],\
                                            "goods_reword" : (get_data("goods_data",id)['price_retail'] - get_data("goods_data",id)['price_buying']) * num
                                            })
    return pd.DataFrame(data_result)
def read_data_recent(df,n=3):
    df_copy = df.copy()
    time_now = datetime.datetime.now()
    for x in df.index:
        sell_time = datetime.datetime.strptime(df_copy.loc[x, "time_stamp"], "%Y-%m-%d %H:%M:%S.%f")
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
    total_sales_per_product = df_copy.groupby('goods_name')['goods_reword'].sum().sort_values(ascending = False )
    # 每类商品的最高销量
    max_sales_per_category = df_copy.groupby(['goods_sort', 'goods_id'])['goods_reword'].sum().groupby('goods_sort').max()

    # 打印结果
    print("每种商品的销售总额:")
    print(total_sales_per_product)

    print("\n每类商品的最高销量:")
    print(max_sales_per_category)


    
def get_predict(df):
    '''
    计时，以n天为界限进行统计。构建预测模型
    '''