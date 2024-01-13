from flaskr.extensions import redis_client,mongo

# from .mongo_operation import data_from_mongo
import json



def clear_all():
    redis_client.flushdb()

def load_data(data):
    '''
    读取data,如果data为json格式则自动转换
    '''
    try:
        json_object = json.loads(data)
    except :
        return data
    return json_object

