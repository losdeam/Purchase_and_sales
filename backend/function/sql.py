from flaskr.extensions import db
from flaskr.models import Goods,Sales_records

dict_sheet = {
    "goods":Goods,
    "sales_records":Sales_records
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
