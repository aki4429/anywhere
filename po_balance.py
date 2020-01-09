#!/usr/bin/env python
# -*- coding: utf-8 -*-

#tfc.sqliteにアクセスして、POバランス表を作ります

import sqlite3
import datetime
import csv
from dateutil import relativedelta
from datetime import date

DB_FILE = 'tfc.sqlite'

con = sqlite3.connect(DB_FILE)
cur = con.cursor()

#balance 初期化
def reset():
    #begin_day = input("発注日でいつより後の発注残を出しますか。(例)20190601:")
    #begin_day = begin_day[:4] + "-" + begin_day[4:6] + "-" + begin_day[6:8]
    year_before = date.today()-relativedelta.relativedelta(years=1) 
    begin_day = year_before.strftime('%Y-%m-%d')
    print('発注日が' + begin_day + '以降の注文残を更新します。')
    #begin_day ='2016-0101'

    #poの発注日以降のbalanceを発注数量に戻す。
    cur.execute("update poline set balance = qty where id in (select l.id from poline l inner join po p on l.po_id = p.id where p.pod > ?) ", (begin_day,))
    con.commit()

    #poline_idを持つ発注日以降deliveryの全インボイス行を抽出
    cur.execute("select v.poline_id, v.qty, i.invn from invline v inner join inv i on v.inv_id = i.id where v.poline_id <> '' and i.delivery > ?", (begin_day,))

    invlines = cur.fetchall()

    #発注日以降のpo内容情報の取得
    cur.execute("select o.id, p.pon, o.qty, c.hinban from ((poline o inner join po p on o.po_id = p.id) inner join tfc_code c on o.code_id = c.id) where p.pod > ?", (begin_day, ))

    polines = cur.fetchall()

    zan_hyo =[]
    balance_hyo = []

    for row in polines:
        zan_hyo.append(list(row))

    for zan in zan_hyo:
        total = 0
        for row in invlines:
            if row[0] == zan[0]:
                zan += [row[1], row[2]] #[qty, invn]
                total += int(float(row[1]))

        bal_qty = int(float(zan[2]))-total
        if bal_qty > 0 :
            zan += [bal_qty]
            balance_hyo.append(zan)
        else:
            #残数がゼロかもっと小さければ
            zan += [0]

    zan_hyo.sort()
    balance_hyo.sort()
    with open('zan_hyo.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(zan_hyo)
        print('zan_hyo.csv=消込リストを書きました。')

    with open('balance_hyo.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(balance_hyo)
        print('balance_hyo.csv=発注残表を書きました。')

    for row in zan_hyo:
        cur.execute("update poline set balance=? where id =?", (row[-1], row[0]))

    con.commit()

    cur.close()
    con.close()

#reset()
