from function.sql import upload_data,get_value, get_values,get_values_time,delete_value,update_data
from flaskr.extensions import redis_client
from flask import jsonify



def warehouse_add(warehouse_sort,warehouse_note):
    '''
    添加全新商品\n
    input:\n
        warehouse_sort :商品id\n
        warehouse_note : 仓库备注\n
    output:\n
        None : 直接对数据库进行操作\n
    '''
    data_result = {}
    data_result["message"] = ""
    upload_data({"warehouse_sort":warehouse_sort,"warehouse_note":warehouse_note})
    return jsonify(data_result)
