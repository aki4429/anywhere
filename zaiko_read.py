#!/usr/bin/env python
# -*- coding: utf-8 -*-

FILE_ZEN="zaiko_d/kento20190516.csv"
FILE_COV="zaiko_d/cover_zaiko.csv"
FILE_NUNOHIN="zaiko_d/nunoji_hinban.csv"
SFILE = "tfc.sqlite"
FILEOUT = "zaiko.csv"

import csv
import hinmoku #品目名クラス・品目コードを加工修正したりするため
import sqlite3
import pandas as pd
from pandas import DataFrame, Series
import numpy as np

class ZaikoRead:
    def __init__(self):
        data = []
        zai_data=[]
        shiire_data=[]
        data = self.read(FILE_ZEN)
        #オリジナル布地番号/フクラコード変換用データ読み込み
        nunodata=self.read_nunohin(FILE_NUNOHIN)

        #材料コードと仕入れコードでデータを切り分ける
        #材料は、品目CD, 現在庫数_自倉庫, 受注数
        #仕入品は、品目名, 現在庫数_自倉庫, 受注数
        for d in data:
            if d[0].startswith('0'):
                zai_data.append([d[0], d[2], d[3]])
            else:
                if len(d[1]) > 1:
                    shiire_data.append([ d[1], d[2], d[3]])

        shiire_changed = self.make_shiire(shiire_data, nunodata)

        #カバーを除く
        cover_removed =[]
        for zai in zai_data:
            if not zai[0].startswith('013CH2'):
                cover_removed.append(zai)

        result_data = cover_removed + shiire_changed

        #self.show(self.result_data)

        #for row in zai_data:
            #print(*row)
        
        #for row in shiire_changed:
        #    print(*row)

        #for row in shiire_data:
        #    if row[0].startswith('CH1'):
        #        print(*row)

        cover_data = self.read_zaiko(FILE_COV)
        #self.show(cover_data)

        result_data = result_data + cover_data 
        result_data.sort()
       
        n = np.array(result_data)
        self.df = DataFrame(n[:, 1:], index=n[:, 0], columns=['在庫','受注'])

        #print(self.df)
        self.df.to_csv("zaiko.csv", encoding="CP932")

        #self.save(self.result_data)

    def read(self, filename):
        data = []
        with open(filename, 'r', encoding='CP932') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader: #品目CD, 品目名, 現在庫数_自倉庫, 受注数
                data.append([row[6], row[7], int(row[14]),int(float(row[118]))])

        return data

    #def pick_zai(self, data):


    def read_nunohin(self, filename):
        nunohin=[]
        with open(filename, 'r', encoding='CP932') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader: #布地番号Before/After
                nunohin.append(row)

        return nunohin
    
    #仕入品のデータは、在庫管理用コード(発注コード）に変換して集計
    def make_shiire(self, shiire_data, nunodata):
        #TFCコードDBから 在庫用コードを取り出しておく
        con = sqlite3.connect(SFILE)
        cur = con.cursor()
        sql = "select hcode from tfc_code where zaiko=1"
        cur.execute(sql)
        results =  cur.fetchall()
        #結果はtuple (xxxx,) なので、取り出すのに[0]
        #とりだしたデータCHXXX-03SET XX/XXX の-以前を取り出す。
        zaikolist = [x[0].split("-")[0] for x in results if not x[0].startswith('0')]
        #重複要素を除く
        zaikolist = list(set(zaikolist))
        #print("zaikolist", zaikolist)
        if '' in zaikolist:
            zaikolist.remove('')

        #末尾の'N'は除く(除いておかないとヒットしないコードあり)
        #CH1071N
        zaikolist = list(map(lambda x: x.replace('N','') if x.endswith('N') else x, zaikolist))

        #print("zaikolist", zaikolist)
        con.close()

        shiire_new = []

        #在庫コードを含むデータだけ、抽出
        for shiire in shiire_data:
            print("shiire[0]", shiire[0])
            if self.check_zaiko(shiire[0], zaikolist):
                shiire_new.append(shiire)

        data =[]
        zaiko = {}
        juchu = {}
        code =""
        #print('shiire_new', shiire_new)
        for row in shiire_new: 
            #row[0]=品目名の読替え必要なものは読み替える
            h = hinmoku.Hinmoku(row[0])
            code = h.make_code()
            for nuno in nunodata:
            #布オリジナル番号は読み替える
                if nuno[0] in code:
                    code = code.replace(nuno[0], nuno[1])

            #在庫辞書があれば在庫数を追加
            if code != "" and code in zaiko:
                zaiko[code] += int(row[1])
            #無ければ作成
            else:
                zaiko[code] = int(row[1])

            #受注辞書があれば受注数を追加
            if code !="" and code in juchu:
                juchu[code] += int(float(row[2]))
            #無ければ作成
            else:
                juchu[code] = int(float(row[2]))

        for k in list(zaiko.keys()):
            for kz, vz in zaiko.items():
                for kj, vj in juchu.items():
                    if k == kz and k == kj:
                        data.append([k, vz, vj])
                        #print(k, vz, vj)

        return data


    def read_zaiko(self, filename):
        data =[]
        with open(filename, 'r', encoding='CP932') as csvfile:
            reader = csv.reader(csvfile)
            #next(reader)
            for row in reader: #品目CD, 現在庫数_自倉庫, 受注数
                data.append([row[0], int(row[1]),int(float(row[2]))])

        return data

    def get_date(self):
        kijunbi =""
        csvfile = open(FILE_ZEN, 'r', encoding='CP932')
        reader = csv.reader(csvfile)
        next(reader)
        kijunbi = next(reader)[18]

        csvfile.close()
        return kijunbi

    def show(self, data):
        for c in data:
            print(*c)

    def check_zaiko(self, code, zaikolist):
        for zaiko in zaikolist:
            if zaiko in code:
                return True

        return False

    def check_cover(self, code, zaikolist):
        for zaiko in zaikolist:
            if zaiko[0] == code:
                return True

        return False

    def save(self, data):
        with open('zaikohyo.csv', 'w') as w:
            writer = csv.writer(w, lineterminator="\n")
            writer.writerows(data)
            
            

#k = ZaikoRead()
#print(k.df)
#print(k.get_date())
#k.show(k.result_data)

