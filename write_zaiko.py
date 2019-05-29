#!/usr/bin/env python
# -*- coding: utf-8 -*-

#在庫報告を作成するプログラム。
#DBからzaiko　フラグのデータをダウンロードする。
#品名、カテゴリーの順番に

DBFILE='tfc.sqlite'

CAT_ORDER = ['布地','ﾇｰﾄﾞ','ｶﾊﾞｰ','INCOON', 'INCOON BED', '脚','ｸｯｼｮﾝ', '旧モデル']

MENU ="""
作成する表を選んでください。
===========================
1) TFC在庫表
2) TFC検討表
--------------------------
番号で選んでください。(1/2/.. or q=終了): """

ZAIKOF = 'zaiko.csv'
KENTOF = 'kento.csv'
ZHYO = 'zaiko_hyo.csv'
KHYO = 'kento_hyo.csv'
KENTO_C = 'kentohyo.csv' #検討表のコード並び
                
import zaiko_read
import make_yotei
import pandas as pd
from pandas import DataFrame, Series
import numpy as np

import sqlite3

class WriteZaiko:
    def __init__(self):
        con = sqlite3.connect(DBFILE)
        cur = con.cursor()

        ans = ''
        while ans != 'q':
            ans = int(input(MENU))
            if ans == 1:
                print("在庫表を作成します")
                input()
                #DB tfc_codeテーブルから在庫フラグがあるデータをゲット
                data = self.get_zaiko(cur)
                zaiko_file_name = ZAIKOF
                hyo_file_name = ZHYO
                ans = 'q'
            else:
                #DB tfc_codeから 検討フラグがあるデータをゲット
                print("検討表を作成します")
                data = self.get_kento(cur)
                zaiko_file_name = KENTOF
                hyo_file_name = KHYO
                ans = 'q'

        data = self.order_by_hcode(data)
        data = self.order_by_cat(data)

        n = np.array(data)
        df = DataFrame(n[:,0],index=n[:,1], columns=['cat'])

        #print(self.df)
        df.to_csv(zaiko_file_name)

        k = zaiko_read.ZaikoRead()

        hyo = df.join([k.df], how='left')
        hyo = hyo.reindex(["在庫", "受注", "cat"], axis=1)
        y = make_yotei.MakeYotei()
        hyo = hyo.join([y.frame], how='left')
        print(hyo)
        if hyo_file_name == KHYO:
            kento_code = pd.read_csv(KENTO_C, index_col='品目CD')
            hyo = kento_code.join(hyo, how='left')

        print('hyo_file_name',hyo_file_name)
        input()
        hyo.to_csv(hyo_file_name, encoding='CP932')
        #hyo.to_csv("kento_hyo.csv")

    def show(self, data):
        for d in data:
            for row in d: 
                print(row[0], row[1])

    def get_zaiko(self, cur):
        #在庫フラグがあるデータをゲット
        cur.execute("select cat, hcode from tfc_code where zaiko=1")
        data = cur.fetchall()
        return data

    def get_kento(self, cur):
        #検討フラグがあるデータをゲット
        cur.execute("select cat, hcode from tfc_code where kento=1")
        data = cur.fetchall()
        return data

    def order_by_hcode(self, data):
        code_data=[]
        sorted_data = []
        for d in data:
            code_data.append(d[1])

        #ファブリックがあれば、ファブリック順に
        #1)モデル名、 2) ファブリック 3) ピース
        fabfirst = lambda val : (val.replace("I-", "-").split("-")[0], val.split(" ")[1] if len(val.split(" ")) > 1 else "")

        code_data.sort(key = fabfirst)

        for cd in code_data:
            for d in data:
                if d[1] == cd:
                    sorted_data.append(d)

        return sorted_data            


    #CAT_ORDER順に並べ替える
    def order_by_cat(self, data):
        ordered_data=[]
        for cat in CAT_ORDER:
            for d in data:
                if d[0] == cat:
                    ordered_data.append(d)

        return ordered_data








w = WriteZaiko()
