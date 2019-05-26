#!/usr/bin/env python
# -*- coding: utf-8 -*-

#受注実績表を読み込み、TFC発注品のみ取り出す

#受注実績データファイル名
#FILENAME="juchu/juchu20190409-15.csv"
FILENAME="juchu/juchu20190416-22.csv"
CODEFILE="tfc_code.csv"
FILEOUT = "kako_juchu.csv"
SQLF = "tfc.sqlite"

#読み出し項目位置(0から数えて)
A_1 = 6 #品目CD
A_2 = 7 #品目名
A_3 = 10 #受注伝票№
A_4 = 12 #受注日
A_5 = 13 #納期
A_6 = 14 #受注数

import csv
import hinmoku #品目名クラス・品目コードを加工修正したりするため
import data_kako
import sqlite3

class JuchuRead:
    def __init__(self, filename):
        self.data = []
        self.codes = []
        self.read(filename) #必要項目をdataに読み出し
        #self.read_cd(CODEFILE) #CODE マスターを読み込み
        self.read_sql(SQLF) #CODE マスターを読み込み
        self.data = data_kako.kako_add(self.data)
        self.data = data_kako.sum(self.data)
        self.data = data_kako.check(self.data, self.codes)
        self.save_juchu(self.data)

    def read(self, filename):
        with open(filename, 'r', encoding='CP932') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader: #品目名,受注伝票№,受注日,納期,受注数
                h = hinmoku.Hinmoku(row[A_2])
                #バイオーダーか確認 and 除外モデルか確認
                if h.is_byorder() and not h.jogai() :
                    self.data.append([h.make_code(),row[A_3],
                        row[A_4],row[A_5],int(float(row[A_6]))])

    def read_cd(self, filename):
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader: 
                self.codes.append(row)

    def read_sql(self, filename):
        con=sqlite3.connect(filename)
        cur = con.cursor()
        #カラム名の一覧取得
        cur.execute('select * from tfc_code where id=1')
        names = [x[0] for x in cur.description]
        #names.pop(0) #idは外す
        sqls = ','.join(names)
        cur.execute("select {} from tfc_code".format(sqls))
        self.codes = list(cur.fetchall())
        con.close()

    def show(self):
        for c in self.data:
            print(c)

    def show_ng(self):
        print("=" * 70)
        for c in self.data:
            if c[5] =="NO" or c[5] == "Double" :
                print(c)

    def save_juchu(self, data):
        # 書き出し用のファイルを開く
        with open(FILEOUT, "a", encoding="CP932") as out_file:
            writer = csv.writer(out_file,lineterminator='\n')
            for row in data:
                writer.writerow(row)


#k = JuchuRead(FILENAME)
#print(k.get_date())
#k.show()
#k.show_ng()
