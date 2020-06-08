#!/usr/bin/env python
# -*- coding: utf-8 -*-

#tfc.sqliteにアクセスして、有益な情報を取り出す。
import sqlite3
import datetime
from dateutil.parser import parse

DB_FILE = 'tfc.sqlite'

class PoStatus:
    def __init__(self):
        con = sqlite3.connect(DB_FILE)
        cur = con.cursor()
        self.menu(cur)
        #self.po_zan(cur)
        con.commit()
        con.close()

    def menu(self, cur):
        idn = ''
        while idn != 'q':
            self.show_po(cur)
            print("="*30)
            idn = input("POのidナンバーを選んでください。(終了~q:)")
            if idn != 'q':
                print('id={} が選ばれました。'.format(idn))
                ans = input("d) 詳細表示 t) 南濃取込日登録 j) 情報取得 q)終了")
                if ans == 'd':
                    self.show_detail(cur, idn)
                elif ans == 't':
                    self.set_deliver(cur, idn)
                elif ans == 'j':
                    self.joho = self.get_info(cur, idn)
                    print('po情報は:', self.joho)
            else:
                print('終了します。')
                pass


    def show_po(self, cur):
        print(" etd  POナンバー  運送手段  港  発注日 ")
        print("="*30)
        cur.execute("select id, etd, pon, per, port, delivery from po order by etd")
        #cur.execute("select id, etd, pon, per, port, pod from po order by etd")
        #cur.execute("select id, etd, pon, per, port,comment, pod from po order by etd")
        res = cur.fetchall()
        res = res[-15:] #最新のデータ○行まで表示
        for row in res:
            cur.execute("select c.uprice * p.qty from poline p inner join tfc_code c on p.code_id = c.id where p.po_id = ?", (row[0],))
            prices = cur.fetchall()
            amount = 0.0
            for  price in prices:
                #print("price",price[0])
                amount += float(price[0])
                
            #print(*row, amount, sep=',')
            print(*row, '{:.2f}'.format(amount)) #下２桁まで

    def show_detail(self, cur, idn):
        print("="*30)
        cur.execute("select i.poline_id, v.invn, i.qty from invline i inner join inv v on i.inv_id = v.id, poline p on i.poline_id = p.id where p.po_id = ?",(idn,))
        ils = cur.fetchall()

        cur.execute("select p.id, c.hinban, p.om, p.qty, p.balance from poline p inner join tfc_code c on p.code_id = c.id where p.po_id = ? ",(idn,))
        pods = cur.fetchall()

        #cur.execute("select p.id, c.hinban, p.om, p.qty, p.balance from poline p inner join tfc_code c on p.code_id = c.id where p.po_id = ? and p.balance >0",(idn,))
        #pods = cur.fetchall()

        status_line =[]
        for pod in pods:
            line =[]
            line.append(pod[0]) #poline_id
            line.append(pod[1]) #品番
            line.append(pod[2]) #OM
            line.append(pod[3]) #数量
            p_qty = float(pod[3])
            for il in ils:
                if il[0] == pod[0]: #poline_idが同じ時 
                    line.append(il[1])  #invナンバー
                    line.append(il[2])  #数量

            line.append("残:")
            line.append(pod[4])
            #print(line)
            status_line.append(line)

        for sline in status_line:
            print(*sline)

        if idn != 'q':
            input("return でメニューに戻ります")

    def po_zan(self, cur):
        print("未入荷リストを表示します。")
        print("="*30)
        cur.execute("select o.pon, c.hinban, p.qty, p.balance, p.om, o.port, o.etd from poline p inner join po o on p.po_id = o.id, tfc_code c on p.code_id = c.id where balance >0 and o.etd < ? order by o.etd ", (datetime.date.today().strftime("%Y-%m-%d"),))
        zans = cur.fetchall()
        print(datetime.date.today().strftime("%Y-%m-%d"))
        for zan in zans:
            print(*zan)

    def set_deliver(self, cur, idn):
        deliver = input("南濃取り込み予定指定してください。例)20190515: ")
        deliver = deliver[:4] + "-" + deliver[4:6] + "-" + deliver[6:8]
        cur.execute("UPDATE po SET delivery = ? where id = ?",(deliver,idn))

    def get_info(self, cur, idn):
        cur.execute("select id, pon, pod, etd, delivery from po where id=?", (idn,))
        joho = cur.fetchone()
        return joho


#s = PoStatus()
#print('情報は', s.joho)

