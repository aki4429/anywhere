#!/usr/bin/env python
# -*- coding: utf-8 -*-

#tfc.sqliteにアクセスして、在庫表・検討表用に入荷予定表を作ります
#南濃取り込み基準日を決めて、それ以降のdelivery納期のpoデータを
#作成します。

import sqlite3
import csv
from index_tool import get_xindex, get_yindex

DB_FILE = 'tfc.sqlite'

class MakeBalance:
    def __init__(self):
        con = sqlite3.connect(DB_FILE)
        cur = con.cursor()

        begin_day = input("南濃着日でいつより後の予定を出しますか。(例)20190601:")
        begin_day = begin_day[:4] + "-" + begin_day[4:6] + "-" + begin_day[6:8]
        #begin_day ='2020-01-06'


        #インボイス残データ用
        #コードの在庫区分が１のインボイス行で、南濃取り込み日が
        #bigin_day より新しいものを抽出
        cur.execute("select i.delivery, i.etd, i.invn, c.hcode, v.qty from ((invline v inner join inv i on v.inv_id = i.id) inner join tfc_code c on c.id = v.code_id) where i.delivery > ? and (c.zaiko=1 or c.kento =1)", (begin_day,))

        invlines = cur.fetchall()
        #self.invlines = invlines

        #インボイスの最新のdeliveryを求めます。
        #（インボイスデータは在庫区分1)
        #POデータはmaxdeli以降

        #cur.execute("select max(i.delivery) from (((invline v inner join poline o on v.poline_id = o.id) inner join po p on p.id = o.po_id) inner join inv i on v.inv_id = i.id) where p.comment = 'To Hukla Japan/Nanno ' and o.om=''")
        cur.execute("select max(i.delivery) from ((invline v inner join inv i on v.inv_id = i.id) inner join tfc_code c on v.code_id = c.id ) where c.zaiko=1 or c.kento=1")
        maxdeli = cur.fetchone()[0]

        #po内容情報の取得/フクラ南濃向けバイオーダー除く
        #id, 着日, etd, PO No. コード　残数
        cur.execute("select o.id, p.delivery, p.etd, p.pon, c.hcode, o.balance from ((poline o inner join po p on o.po_id = p.id) inner join tfc_code c on o.code_id = c.id) where p.delivery > ? and p.comment like '%Nanno%' and o.om = ''", (maxdeli, ))

        polines = cur.fetchall()
        #polines.sort()

        self.zan_hyo =[] #PO情報にinv情報を加えた表を作成
        bal_hyo =[] #残が０より大きいデータのみ格納

        for row in polines: #PO情報をtupleからlistに変換
            #polines情報をzan_hyoに格納
            self.zan_hyo.append(list(row))

        for zan in self.zan_hyo:
            if zan[5] > 0 and not zan[4] =='' : #hcodeがないものは飛ばす
                #残数量がゼロより大きい時、着日, etd, PO No. コード　残数
                bal_hyo.append([zan[1], zan[2], zan[3], zan[4], zan[5]])

        invlist = [] #インボイス情報をtupleからlistに変換
        for row in invlines:
            invlist.append(list(row))

        self.invlist = invlist
        #PO残情報とinv情報を合わせる
        self.totallist = self.sum_list(invlist + bal_hyo)
        #self.totallist.sort()

        cur.close()
        con.close()


    def make_nolist(self):
        #インボイスナンバー、POナンバー,delivery, etdの重複しないリスト
        nos = set()
        for row in self.totallist:
            nos.add((row[0], row[1], row[2]))

        nolist=list(nos)
        nolist.sort()
        #print('nolist:', nolist)
        return nolist

    def make_codelist(self):
        #コードのの重複しないリスト
        codes = set()
        for row in self.totallist:
            codes.add(row[3])

        codelist=list(codes)
        codelist.sort()
        return codelist

    def make_yotei(self):
        nolist = self.make_nolist()
        codelist = self.make_codelist()
        #print('nolist:', nolist)
        #print('codelist:', codelist)

        #予定表用の2次元配列を初期化してデータを代入する
        yotei_hyo = [['' for i in range(len(nolist)+1)] for j in range(len(codelist)+1)]

        #codelist.insert(0, "") #先頭行はタイトル行なので空けておく
        #1列目にコードを代入
        for i, code in enumerate(codelist):
            yotei_hyo[i+1][0] = code

        #１行目にINV no. PO no. を代入
        for i, num in enumerate(nolist):
            yotei_hyo[0][i+1] = num[2]

        #print('self.totallist', self.totallist)

        for row in self.totallist: #着日, etd, PO No. コード　残数
            yotei_hyo[get_yindex(yotei_hyo, row[3])][get_xindex(yotei_hyo, row[2])] = row[4]

        return yotei_hyo


    def write_balance(self, hyo):
        with open('balance.csv', 'w', encoding='CP932') as f:
            writer = csv.writer(f)
            writer.writerows(hyo)

    #ETD, delivery, PO/inv, code, qty
    def sum_list(self, data):
        #コード,PO/INVが同じデータの入荷予定数を加算して一つにまとめる。
        matome ={}  #tuple をキーの辞書
        c_data = [] #まとめたデータ保管用変数

        for row in data:
            matome.setdefault((row[0], row[1], row[2], row[3]), 0 )
            matome[(row[0], row[1], row[2], row[3])] +=  row[4]

        #辞書からリストに戻す
        for k, v in matome.items():
            c_data.append(list(k) + [v])

        return c_data



#mb = MakeBalance()
#mb.write_balance( mb.make_yotei())
#mb.write_balance(mb.totallist)

