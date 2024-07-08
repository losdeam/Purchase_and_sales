from flaskr.extensions import logging
import json
import datetime
import time 


    
def write_log():
    ans = []
    for rank,log in logging.items():
        ans += log
    ans.sort()
    # 打开（或创建）一个文本文件，模式为写入（'w'）
    with open('logging.txt', 'w', encoding='utf-8') as file:
        # 循环遍历列表，逐行写入元素
        for item in ans:
            file.write(item + "\n")




def load_data(data):
    '''
    读取data,如果data为json格式则自动转换
    '''
    try:
        json_object = json.loads(data)
    except :
        return data
    return json_object

