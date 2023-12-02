
from flaskr.extensions import db


class Goods(db.Model): # 商品模型
    __tablename__ = 'goods' 
    good_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    good_name = db.Column(db.String(100), index=True)
    good_num = db.Column(db.Integer)
    good_price_buying = db.Column(db.FLOAT)
    good_price_retail = db.Column(db.FLOAT)
    good_sort = db.Column(db.String(100))
    good_baseline = db.Column(db.Integer)


class Sales_records(db.Model):
    __tablename__ = 'sales_records' 
    time_stamp = db.Column(db.DateTime, primary_key=True, index=True)
    good_id = db.Column(db.Integer,nullable=False)
    good_num = db.Column(db.Integer)
