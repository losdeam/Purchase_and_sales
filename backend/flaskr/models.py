#-*- coding:utf-8 -*-
# author:Agam
# datetime:2018-11-05
from flaskr.extensions import db
from flask_login import UserMixin


class User(db.Model, UserMixin): # 用户模型
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(100), unique=True)
    user_pwd = db.Column(db.String(100))
    user_mail = db.Column(db.String(100))
    user_phone = db.Column(db.String(100))
    user_addtime = db.Column(db.DateTime, index=True)
    user_photo = db.Column(db.LargeBinary)
    rank = db.Column(db.Integer, nullable=False, default=1)




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
    good_id = db.Column(db.Integer,db.ForeignKey('goods.good_id'),nullable=False)
    good_num = db.Column(db.Integer)
