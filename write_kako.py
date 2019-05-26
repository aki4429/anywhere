#!/usr/bin/env python
# -*- coding: utf-8 -*-

#加工済み受注データkako_juchu.csvを読み込み、
#該当するコードデータをtfc_code.csvより抽出
#PO書き出しデータをアウトプットする

#受注実績データファイル名
FILEK="kako_juchu.csv" #加工後受注データ
FILEC="tfc_code.csv"  #TFCコードファイル
FILES="tfc.sqlite"  #コードDBファイル
FILEF="hukla_tfc_fab.csv" #ファブリック照合ファイル
FILEOUT = "po_lines_keep.csv" #書き出しファイル

#読み出し項目位置(0から数えて)
A_0 = 0 #品目名
A_1 = 1 #受注伝票№
A_2 = 2 #受注日
A_3 = 3 #納期
A_4 = 4 #受注数
A_5 = 5 #ok
A_6 = 6 #id

import csv
import code
import sqlite3
import pandas as pd
from pandas import DataFrame, Series

class WriteKako:
    def __init__(self):
        self.kakodata = [] #加工受注データ格納用
        self.fablist = [] #ファブリック変換データ格納用 
        self.codes = [] #TFCコードデータ格納用
        self.read_kako(FILEK) #加工受注データ読み込み
        self.read_fab(FILEF) #ファブリック変換データ
        self.read_code(FILEC) #TFCコード読み込み

    #加工後受注ファイル読み込み
    def read_kako(self, filename):
        with open(filename, 'r', encoding='CP932') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader: #品目名,受注伝票№,受注数,id
                self.kakodata.append([row[A_0], row[A_1], int(row[A_4]), row[A_6]])
                #self.kakodata.append(row)

    # ファブリック変換用ファイルを開く
    def read_fab(self, filename):
        with open(filename, "r") as fl:
        #リストに読み込み
            reader = csv.reader(fl)
            for row in reader:
                self.fablist.append(row)

    #コードファイル読み込んで、csvリスト(data) に格納
    def read_code(self, filename):
        con = sqlite3.connect(FILES)
        df = pd.read_sql("select * from tfc_code", con)
        i=0
        while i < len(df) :
            row = df.iloc[i]
            cd = code.Code(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]) 
            self.codes.append(cd)
            i += 1

    def write_kako(self):
        for data in self.kakodata :
            for code in  self.codes :
                if data[0] in code.get_hinban() :
                    code.write_poline(FILEOUT, self.fablist, data[1], data[2])
        
    def write_kako_sql(self):
        #コードDBに接続
        con = sqlite3.connect(FILES)
        cur = con.cursor()
        counter = 0
        for data in self.kakodata :
            cur.execute('select * from tfc_code where id = ?', (int(data[3]),))
            result = cur.fetchone()
            self.write_poline(FILEOUT, self.fablist, data[1], data[2], result)
            counter += 1

        con.close()
        print("{}行のデータを書き込みました".format(counter))

    def write_poline(self, filename, fablist, om, qty, result):
        poline = []
        poline.append(result[1]) #品番
        poline.append(result[2]) #item
        poline.append(result[3]) #description
        poline.append(result[4]) #remark
        poline.append(qty)
        poline.append(result[5]) #unit
        poline.append(result[6]) #u.price
        poline.append("")
        poline.append("")
        poline.append(self.make_our_item(fablist, result[1]))
        poline.append("")
        poline.append(om)
        poline.append("")
        poline.append(result[8]) #vol
        poline.append(result[0]) #id
        #self.show_poline(poline)
        #print(poline)
        self.save_poline(filename, poline)

    def make_our_item(self, fablist, hinban):
        our_item = hinban
        for fline in fablist:
             our_item = our_item.replace(fline[0], fline[0] + "[" + fline[1] + "]")
        return our_item

    def save_poline(self, filename, poline):
        # 書き出し用のファイルを開く
        with open(filename, "a", encoding="CP932") as out_file:
            writer = csv.writer(out_file,lineterminator='\n')
            writer.writerow(poline)

    def show(self, data):
        for row in data:
            print(row)


w = WriteKako()
w.write_kako_sql()
