#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

engine = create_engine('sqlite:///tfc.sqlite')

Base = declarative_base()

CAT_ORDER = {'布地':1,'ﾇｰﾄﾞ':2,'ｶﾊﾞｰ':3,'INCOON':4, 'INCOON BED':5, '脚':6,'バネ':7, 'ｸｯｼｮﾝ':8, 'HYPERFLEX':9,'ﾛｻﾞｰﾅ':10, '旧モデル':11, '':12}

class TfcCode(Base):
    __tablename__ = 'tfc_code'

    id = Column(Integer, primary_key=True)
    hinban = Column(String(50))
    item = Column(String(50))
    description = Column(String(50))
    remarks = Column(String(50))
    unit = Column(String(10))
    uprice = Column(String(30))
    ouritem = Column(String(30))
    vol = Column(String(10))
    zaiko = Column(String(10))
    kento = Column(String(10))
    hcode = Column(String(50))
    cat = Column(String(30))

    def __repr__(self):
        return "[id:'%s' hinban:'%s' description:'%s' cat:'%s']" % (self.id, self.hinban, self.description, self.cat)

Base.metadata.create_all(engine)

# SQLAlchemy はセッションを介してクエリを実行する
Session = sessionmaker(bind=engine)
session = Session()

def get_z():
    #在庫フラグのコードを取得
    result = session.query(TfcCode.hcode, TfcCode.cat).filter(TfcCode.zaiko ==1).all()
    #print('result', result)
    return result

def get_k():
    #検討フラグのコードを取得
    result = session.query(TfcCode.hcode, TfcCode.vol, TfcCode.cat).filter(TfcCode.kento ==1).all()
    #print('result', result)
    return result

session.close()

def ori_sort(result):
    catn = lambda val:CAT_ORDER[val[-1]]
    model = lambda val:val[0].split('-')[0].replace('I', '')
    pie = lambda val:val[0].split('-')[-1] 
    fab = lambda val:val[0].split(' ')[-1]
    result = sorted(result, key=pie)
    result = sorted(result, key=fab)
    result = sorted(result, key=model)
    result = sorted(result, key=catn)
    return result

def print_menu(result):
    if len(result[0]) == 2:
        for row in result:
            print(row[0], row[1])

    elif len(result[0]) == 3:
        for row in result:
            print(row[0], row[1], row[2])

#print_menu(get_k())
#print_menu(ori_sort(get_z()))
