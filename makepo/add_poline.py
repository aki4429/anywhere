#!/usr/bin/env python
# -*- coding: utf-8 -*-

#po_linesファイルからデータを読みこんで、polineを追加。

import os
import csv 
import datetime
import poline
import po
import sqlite3

#file_name = tools.get_latest_modified_file_path(os.curdir, "*xl*")
POLINES = "../po_lines_keep.csv"
PONOFILE = "pono.txt"
TFCS = "../../tfc_sql/tfc.sqlite"

ITEMROWBEGIN = 16 #アイテム行は１から数えて何番目から
ITEMCOLUMNBEGIN = 2 #アイテム列は、A=１から数えて何番目

PODATE ="J6"

MAX = 300 #ベースPOのアイテム行の最後行 index

class AddPoline:
    def __init__(self):
        poid = input("追加するPOの id を入力してください。")
        po_data = self.read_lines(POLINES)
        self.show_podata(po_data)
        self.write_posql(poid, po_data)

    def write_posql(self, poid, po_data):
        con = sqlite3.connect(TFCS)
        cur = con.cursor()

        for pl in po_data:
            if pl.code_id == '':
                cur.execute("select id from tfc_code where item = ?",
                        (pl.item,))
                codeid = cur.fetchone()[0]
            else:
                codeid = pl.code_id
                print("codeid", codeid)

            cur.execute('INSERT INTO poline (code_id, qty, remark, om, balance,po_id) VALUES(?, ?, ?, ?, ?, ?)', (codeid, pl.qty, pl.remarks, pl.om, pl.qty, poid ))

        con.commit()
        con.close()


    #発注データpo_linesの読み込み
    def read_lines(self, filename):
        data = []
        with open(filename, 'r', encoding='CP932') as f:
            reader = csv.reader(f)
            for row in reader: 
                pl = poline.Poline(*row)
                #print('pl.code_id', pl.code_id == '')
                data.append(pl)

        return data

    def show_podata(self, po_data):
        for pl in po_data:
            pl.show_line()

    #def set_conditions(self):
        

a = AddPoline()
