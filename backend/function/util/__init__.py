from .mongo_operation import *
from .yaml_operation import *
from .local_operation import * 
from .redis_operation import *
from .password_operation import * 
from .tools import *

def data_update(goods_id,num):
    data_result = {}
    final_data = data_from_mongo('goods_data',{'id' :goods_id}) [0]
    final_data['num'] = num
    data_result["message"] = data_update_mongo(goods_id,"goods_id","goods_data",final_data)
def redis_to_mongo():
    collection_name = 'goods_num'
    for id,val in redis_client.hgetall(collection_name).items():
        id = int(id)
        val = {int(val)}
        data_update(id,val)

def clear_all():
    logging[0].append(f"{datetime.datetime.now()}-----正在将redis中的数据转移至mongo中")
    redis_to_mongo()
    logging[0].append(f"{datetime.datetime.now()}-----转移成功,已清空redis数据库")
    time.sleep(0.0001)
    logging[0].append(f"{datetime.datetime.now()}-----正在将本次运行日志写入logging.txt")
    write_log()
    time.sleep(0.0001)
    redis_client.flushdb() # 清空redis数据库