#!/usr/bin/env python
# -*- coding: utf-8 -*-

#受注実績表を読み込み、TFC発注品のみ取り出す

#受注実績データファイル名
#FILENAME="juchu/juchu20190409-15.csv"
#FILENAME="juchu_20191105.csv"
#FILENAME="juchu_20191028.csv"
FILEOUT = "kako_juchu.csv"
SQLF = "tfc.sqlite"

#読み出し項目位置(0から数えて)
#A_1 = 6 #品目CD
#A_2 = 66 #品目名
A_3 = 1 #受注伝票№
A_4 = 0 #受注日
A_5 = 29 #納期(出荷日)
A_6 = 73 #受注数
A_7 = 34 #倉庫コード

HIN=56 #品目CD
SHI=57 #仕様
PIE=58 #ピース
PAR=59 #パーツ
IRO=60 #色
NU1=61 #布地1
NU2=62 #布地2
TOK=63 #特


import csv
import hinmoku_2 #品目名クラス・品目コードを加工修正したりするため
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
        #print('self.data:', self.data)
        self.save_juchu(self.data)

    def read(self, filename):
        with open(filename, 'r', encoding='CP932') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader: #品目名,受注伝票№,受注日,納期,受注数
                #print("row={0}:".format(A_2) + row[A_2])
                hinmoku_data=[]
                hinmoku_data.append(row[HIN])
                hinmoku_data.append(row[SHI])
                hinmoku_data.append(row[PIE].zfill(2))
                hinmoku_data.append(row[PAR])
                hinmoku_data.append(row[IRO])
                hinmoku_data.append(row[NU1])
                hinmoku_data.append(row[NU2])
                hinmoku_data.append(row[TOK])
                h = hinmoku_2.Hinmoku(hinmoku_data)
                #h.print_detail()
                #バイオーダーか確認 and 除外モデルか確認
                #倉庫コードがA10000か
                if (h.is_byorder() or h.is_fujiei() ) and row[A_7] == 'A10000' and not h.jogai() :
                    self.data.append([h.make_code(),row[A_3],
                        row[A_4],row[A_5],int(float(row[A_6]))])

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
