#!/usr/bin/env python
# -*- coding: utf-8 -*-

#POを指定して、そのpoline のbalance に発注数を
#セットし、該当するinvline の数量を減らす

import sqlite3

SFILE = "tfc.sqlite"

class BalanceReset:
    def __init__(self):
        #DB準備
        con = sqlite3.connect(SFILE)
        cur = con.cursor()

        #POナンバー取得
        pon = ''
        while pon != 'q':
            pon = input("PO#を指定してください。(終了=>q): ")
            if pon == 'q':
                continue
            else:
                poid = self.check_pon(cur, pon)
                if poid == None:
                    input("そのPO#はありません。再度入力してください。")
                    continue
                else:
                    self.set_default(cur, poid)
                    con.commit()
                    self.reduce_invline(cur, poid)
                    con.commit()

        con.close()

    def check_pon(self, cur, pon):
        cur.execute("select id from po where pon = ?",(pon,))
        results = cur.fetchone()
        if results == None:
            return None
        else:
            return results[0]
    
    #そのPOのpoline のbalance を発注数にすべてリセットする。
    def set_default(self, cur, poid):
        cur.execute("UPDATE poline SET balance = qty WHERE po_id = ?",\
                (poid,))

    def reduce_invline(self, cur, poid):
        #該当するpoline id を全て取得
        cur.execute("select id from poline where po_id = ?", (poid,))
        plids = cur.fetchall()
        #poline id 毎にbalance から invline の数量合計を引いて更新
        for plid in plids:
            cur.execute("UPDATE poline SET balance = balance - ( SELECT \
                    SUM(qty) FROM invline WHERE poline_id = ?) WHERE id = ? \
                    and EXISTS (SELECT 1 FROM invline WHERE poline_id = ?) ", \
                    (plid[0], plid[0], plid[0]))



b = BalanceReset()
