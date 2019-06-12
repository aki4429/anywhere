#!/usr/bin/env python
# -*- coding: utf-8 -*-

#tfc.sqliteにアクセスして、有益な情報を取り出す。

import sqlite3
import datetime
from dateutil.parser import parse

DB_FILE = 'tfc.sqlite'

class InvStatus:
    def __init__(self):
        con = sqlite3.connect(DB_FILE)
        cur = con.cursor()
        self.menu(cur)
        con.commit()
        con.close()

    def show_inv(self, cur):
        cur.execute("select * from inv order by etd")
        res = cur.fetchall()
        for row in res:
            print(*row)

    def menu(self, cur):
        idn = ''
        while idn != 'q':
            self.show_inv(cur)
            print("="*30)
            idn = input("インボイスのidナンバーを選んでください。")
            if idn != 'q':
                ans = input("d) 詳細表示 t) 南濃取込日登録 q)終了")
                if ans == 'd':
                    self.show_detail(cur, idn)
                elif ans == 't':
                    self.set_deliver(cur, idn)
            else:
                pass

    def show_detail(self, cur, idn):
        print("="*30)
        cur.execute("select c.hinban, i.qty, o.pon, p.qty, p.om, c.id from invline i inner join tfc_code c on i.code_id = c.id, poline p on i.poline_id = p.id, po o on p.po_id = o.id  where inv_id = ?",(idn,))
        res = cur.fetchall()
        for row in res:
            if row[4] == None:
                om = '在庫分'
            else:
                om = row[4]
            print(row[0], row[1], row[2], row[3],om, row[5] )

        input("returnでメニューｎ戻ります。")

    def set_deliver(self, cur, idn):
        deliver = input("南濃取り込み予定指定してください。例)20190515:")
        deliver = deliver[:4] + "-" + deliver[4:6] + "-" + deliver[6:8]
        cur.execute("UPDATE inv SET delivery = ? where id = ?",(deliver,idn))

#s = InvStatus()
