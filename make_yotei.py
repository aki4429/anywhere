#!/usr/bin/env python
# -*- coding: utf-8 -*-

#tfc.sqliteにアクセスして、入荷予定表を作ります
#南濃取り込み基準日を決めて、それ以降の取り込みの
#インボイスデータとPOデータから品名、入荷予定日、数量の
#マトリックス表を作成します。

import sqlite3
import datetime
from dateutil.parser import parse
import pandas as pd
from pandas import DataFrame, Series

DB_FILE = 'tfc.sqlite'

MENU = """
1)
"""

class MakeYotei:
    def __init__(self):
        con = sqlite3.connect(DB_FILE)
        cur = con.cursor()
        inv_data = self.get_inv_yotei(cur)

        #入手インボイスの最新のETDを求めます。
        #インボイスデータをmaxetdまで、POデータはmaxetd以降
        cur.execute("select max(etd) from inv")
        maxetd = cur.fetchone()[0]
        #print('maxetd', maxetd)

        po_data = self.get_po_yotei(cur, maxetd)
        self.get_po_zan(cur, maxetd)

        yotei_data = inv_data + po_data
        self.frame = self.kako_data(yotei_data)
        #print("yotei_data", yotei_data)
        #self.menu(cur)
        #con.commit()
        con.close()

    def get_inv_yotei(self, cur):
        data=[]
        begin_day = input("南濃着日でいつより後の予定を出しますか。(例)20190601:")
        begin_day = begin_day[:4] + "-" + begin_day[4:6] + "-" + begin_day[6:8]
        cur.execute("select c.hcode, l.qty, i.delivery, i.etd, i.invn from invline l inner join inv i on l.inv_id = i.id, tfc_code c on l.code_id = c.id, poline p on l.poline_id = p.id where i.delivery > ? and c.kento = 1 and (p.om = '' or p.om IS NULL)", (begin_day,))
        #cur.execute("select c.hcode, l.qty, i.delivery, i.etd, i.invn from invline l inner join inv i on l.inv_id = i.id, tfc_code c on l.code_id = c.id, poline p on l.poline_id = p.id where i.delivery > ? and c.zaiko = 1 ", (begin_day,))
        yoteis = cur.fetchall()
        print("INVOICE 予定")
        print("="*30)
        for yotei in yoteis:
            print(*yotei)
            data.append([yotei[0], yotei[1], yotei[2], yotei[3], yotei[4]])

        return data

    def get_po_yotei(self, cur, maxetd):
        data=[]
        cur.execute("select c.hcode, p.qty, o.delivery, o.etd, o.pon from poline p inner join po o on p.po_id = o.id, tfc_code c on p.code_id = c.id where o.etd > ? and kento = 1 and (p.om = '' or p.om IS NULL)", (maxetd,))
        yoteis = cur.fetchall()
        print("PO 予定")
        print("="*30)
        for yotei in yoteis:
            print(*yotei)
            data.append([yotei[0], yotei[1], yotei[2], yotei[3], yotei[4]])

        return data

    def get_po_zan(self, cur, maxetd):
        cur.execute("select c.hcode, p.balance, o.delivery, o.etd, o.pon from poline p inner join po o on p.po_id = o.id, tfc_code c on p.code_id = c.id where o.etd <= ? and kento = 1 and (p.om = '' or p.om IS NULL) and balance >0", (maxetd,))
        yoteis = cur.fetchall()
        print("出荷残リスト")
        print("="*30)
        for yotei in yoteis:
            print(*yotei)

    def kako_data(self, data):
        #南濃取り込み日付を取り出して重複を除いてソート
        hiduke =[]
        for d in data:
            hiduke.append(d[2])
            
        hiduke = sorted(set(hiduke))
        print("hiduke",hiduke)
        
        #南濃取り込み日付が該当するETDをゲット
        self.etds = []
        for hi in hiduke:
            flag =0
            for d in data:
                if d[2] == hi and flag == 0 :
                    self.etds.append(d[3])
                    flag = 1


        #南濃取り込み日付が該当するPO#または、INV#をゲット
        self.pos = []
        for hi in hiduke:
            flag =0
            for d in data:
                if d[2] == hi and flag == 0 :
                    self.pos.append(d[4])
                    flag =1


        #コードを取り出して重複を除いてソート
        codes =[]
        for d in data:
            codes.append(d[0])
            
        codes = sorted(set(codes))
        #print("code",codes)
        
        #コードと日付をキーにしてネストした予定辞書を初期化します。
        yotei={}
        for d in hiduke:
            yotei.setdefault(d, {})
            for code in codes:
                yotei[d].setdefault(code,'')

        #DataFrame に値を挿入します。
        frame = DataFrame(yotei)
        for d in data:
            if frame.at[d[0],d[2]] == '':
                frame.at[d[0],d[2]] = d[1]
            else:
                frame.at[d[0],d[2]] += d[1]

        #print(frame)
        frame.to_csv("yotei_frame.csv")

        return frame

        

#m= MakeYotei()
#print('etds',m.etds)
#print('pos',m.pos)

