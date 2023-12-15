from flaskr.extensions import db
from flaskr.models import Goods,Sales_records,User

dict_sheet = {
    "goods":Goods,
    "sales_records":Sales_records,
    "user": User
}
def upload_data(data, sheet):
    '''
    data:dict
    sheet:str
    将data中的数据上传数据库的sheet表中
    '''
    if sheet in dict_sheet:
        stmt = db.insert(dict_sheet[sheet]).values(data)
    else:
        raise AttributeError("sheet name error")

    db.session.execute(stmt)
    db.session.commit()

    pass
def get_value(data, key, sheet):
    '''
    根据所给的data值在sheet的key字段中寻找一条记录
    return : 字典格式的记录,不存在则返回None
    '''
    if sheet in dict_sheet:
        stmt = db.select(dict_sheet[sheet]).where(getattr(dict_sheet[sheet], key) == data)
    else:
        raise AttributeError("sheet name error")

    result = db.session.execute(stmt).scalar_one_or_none()

    return result
def get_values(data, key, sheet):
    '''
    根据所给的data值在sheet的key字段中寻找所有符合的记录
    return : 字典格式的记录,不存在则返回None
    '''
    if sheet in dict_sheet:
        stmt = db.select(dict_sheet[sheet]).where(getattr(dict_sheet[sheet], key) == data)
    else:
        raise AttributeError("sheet name error")

    result = db.session.execute(stmt).all()

    if result:
        return result
    else:
        return None
def get_values_time(data, key, sheet):
    '''
    根据所给的data值在sheet的key字段中寻找所有符合的记录
    return : 字典格式的记录,不存在则返回None
    '''
    if sheet in dict_sheet:
        stmt = db.select(dict_sheet[sheet]).where(getattr(dict_sheet[sheet], key) >= data)
    else:
        raise AttributeError("sheet name error")

    result = db.session.execute(stmt).all()

    if result:
        return result
    else:
        return None
def update_data(data, key, sheet,new_data):
    data_result = []
    stmt = db.select(dict_sheet[sheet]).where(getattr(dict_sheet[sheet], key) == data)
    result = db.session.execute(stmt).scalar_one_or_none()
    if result != None:
        for key, value in new_data.items():
            if value:
                try :
                    setattr(result, key, value)
                    data_result.append(f"修改成功,已成功将{sheet}表中的{key}字段修改为{value}")
                except:
                    data_result.append(f"修改失败,修改{sheet}表中的{key}字段修改为{value}时出现问题")
        # 提交更改
        db.session.commit()
    return data_result
def delete_value(data, key, sheet):
    '''
    从sheet表中找到与key字段中与data相匹配的记录，并删除
    return : boolean
    '''
    record = get_value(data, key, sheet)
    if record:
        db.session.delete(record)
        db.session.commit()
        return True 
    return False 
def get_all(key,sheet):
    '''
    返回所有在sheet的key字段中的记录的对应值
    return : 字典格式的记录,不存在则返回None
    '''
    if sheet in dict_sheet:
        result = dict_sheet[sheet].query.all()
    else:
        raise AttributeError("sheet name error")

    if result:
        return [getattr(record, key) for record in result]
    else:
        return None