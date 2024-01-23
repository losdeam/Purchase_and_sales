from flaskr.extensions import redis_client
# from instance.yolo_config import path_config,data_config,train_config
from flaskr.extensions import  login_manager
from flask_login import logout_user, login_required, current_user
from .tools import load_data

import json
import yaml

# def josn_read(data):

def get_config_data (config_name,argument):
    '''
    获取对应config_name名称的参数键值
    '''
    if  current_user.is_authenticated:
        
        user_data = redis_client.hget('user_data', current_user.name)
        # print(user_data)
        argument_data = json.loads(user_data)[config_name]
        # print(json.loads(argument_data))
        return json.loads(argument_data)[argument]
    # print(current_user.__dir__())
    return False 

def get_data(sheet, key):
    '''
    获取sheet表中的key键的值
    '''
    # print(sheet, key)
    # print(redis_client.hget(sheet, key))
    return load_data(redis_client.hget(sheet, key))





