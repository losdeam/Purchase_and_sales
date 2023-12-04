
from flaskr.extensions import db


class Goods(db.Model): # 商品模型
    __tablename__ = 'goods' 
    Warehouse_id = db.Column(db.Integer,db.ForeignKey('Warehouse.Warehouse_id') ,primary_key=True)
    good_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    good_name = db.Column(db.String(100), index=True)
    good_num = db.Column(db.Integer)
    good_price_buying = db.Column(db.FLOAT)
    good_price_retail = db.Column(db.FLOAT)
    good_sort = db.Column(db.String(100))
    good_baseline = db.Column(db.Integer)
    good_note = db.Column(db.String(200))


class Sales_records(db.Model):
    __tablename__ = 'sales_records' 
    time_stamp = db.Column(db.DateTime, primary_key=True, index=True)
    good_id = db.Column(db.Integer,nullable=False)
    good_num = db.Column(db.Integer)

class User(db.Model):
    __tablename__ = 'user' 
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    rank = db.Column(db.Integer, nullable=False, default=1)
    power = db.Column(db.String(100), nullable=False)


class Warehouse(db.Model):
    __tablename__ = 'warehouse' 
    warehouse_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    warehouse_sort = db.Column(db.String(100))
    warehouse_note = db.Column(db.String(200))