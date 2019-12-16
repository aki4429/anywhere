#!/usr/bin/env python
# -*- coding: utf-8 -*-

#インボイスを読み込んで、品名、数量のデータを取り出す
#データDBに登録し、登録結果を保存する

import sqlite3
import os
import xlrd
import datetime
from dateutil.parser import parse


#０から数えてデータが始まる行
BEGIN_ROW = 12
CONTAINER_ROW = 2

#品名、数量はゼロから数えて左から何列目？
PO_COL = 0
ITEM_COL = 2
QTY_COL = 3
#UP_COL = 5

INVN = (2,0) #inv.#位置
ETD = (9,0) #ETD位置

SHEET_NAME = "INVOCE"
SFILE = "tfc.sqlite"

class ReadInv:
    def __init__(self):
        #パス付きファイル名取得
        full_names = [os.path.join("invoice", x) for x in os.listdir("invoice")]

        con = sqlite3.connect(SFILE)
        cur = con.cursor()

        #invoiceフォルダの全ファイルに実行
        for file_name in full_names:
            book = xlrd.open_workbook(file_name)
            #print(book.sheet_names())
            sheet = book.sheet_by_name(SHEET_NAME)

            invn = self.get_invn(sheet)
            etd = self.get_etd(sheet)

            containers = self.ifcontainers(book)

            if containers == 0 :
                invid = self.insert_inv(sheet, con, cur, invn, etd)
                con.commit()

                self.insert_invline(sheet, con, cur, invid, BEGIN_ROW)
                #con.commit()
            else:
                for i in range(1, containers + 1):
                    sheet = book.sheet_by_name('Container' + str(i))
                    invid = self.insert_inv(sheet, con, cur, invn+str(i), etd)
                    self.insert_invline(sheet, con, cur, invid, CONTAINER_ROW)


        con.close()

    def get_invn(self, sheet):
        return sheet.cell(*INVN).value.replace("Invoice No:","")
        
    def get_etd(self, sheet):
        etd = parse(sheet.cell(*ETD).value.replace("ETD:","" ))
        return etd.strftime("%Y-%m-%d")

    def ifcontainers(self, book):
        sheets = book.sheet_names()
        counter = 0
        for sn in sheets:
            if 'Container' in sn:
                counter += 1

        return counter

    #インボイスデータ(Inv.NO. ETD)をDBに登録、idを返す。
    def insert_inv(self, sheet, con, cur, invn, etd):
        cur.execute("INSERT INTO inv (invn, etd) VALUES(?,?)", (invn, etd))
        con.commit()
        print("invn", invn)
        return cur.lastrowid

    def insert_invline(self, sheet, con, cur, invid, begin_row):
        #データ始まり行から最終行まで
        keep_pon=""
        for row_index in range(begin_row, sheet.nrows):
            pon = sheet.cell(row_index, PO_COL).value
            #PO NO. ブランク行は、上のセルのPO NO.
            if len(pon) != 0:
                keep_pon = pon
            else:
                pon = keep_pon

            item = sheet.cell(row_index, ITEM_COL).value
            #CHは旧コードに変換
            item = item.replace("CH271E-03B", "CH271-03B")
            item = item.replace("CH271E-08B", "CH271N-08B")
            item = item.replace("CH271E-09B", "CH271N-09B")
            item = item.replace("CH271E-41B", "CH271-41B")
            item = item.replace("CH271E-42B", "CH271-42B")
            item = item.replace("CH271E-49B", "CH271N-49B")
            item = item.replace("CH271E-50B", "CH271N-50B")
            item = item.replace("CH271E-17B", "CH271-17B")
            item = item.replace("CH271E-03 ", "CH271-03 ")
            item = item.replace("CH271E-08 ", "CH271N-08 ")
            item = item.replace("CH271E-09 ", "CH271N-09 ")
            item = item.replace("CH271E-41 ", "CH271-41 ")
            item = item.replace("CH271E-42 ", "CH271-42 ")
            item = item.replace("CH271E-49 ", "CH271N-49 ")
            item = item.replace("CH271E-50 ", "CH271N-50 ")
            item = item.replace("CH271E-17 ", "CH271-17 ")
            qty = sheet.cell(row_index, QTY_COL).value
            #Item 列のセルが空白になったら、終わり
            if len(item) == 0 :
                break
            else:
                #code_id取得
                cur.execute("select id from tfc_code where item = ?", (item,))
                codeid = cur.fetchone()
                if codeid == None:
                    codeid = ""
                else:
                    codeid = codeid[0]
                #poline id 取得
                cur.execute("select p.id from poline p inner join tfc_code\
                        c on p.code_id = c.id, po o on p.po_id = o.id\
                        where o.pon = ? and c.item = ? and p.balance > 0 ", (pon, item))
                polineid = cur.fetchall()
                if len(polineid) >0 :
                    polineid = polineid[0][0]
                else:
                    polineid = ""
                #インボイス行の登録
                cur.execute("INSERT INTO invline ( code_id , qty,\
                        inv_id, poline_id , item ) VALUES( ?, ?, ?, ?, ?)",
                        (codeid, qty, invid, polineid, item))
                #PO行の残を減らします。
                cur.execute("UPDATE poline SET balance = (balance - ?) where id = ? ", (qty, polineid))
                con.commit()
                print("Writing..", item, codeid, polineid, qty)
                continue


r = ReadInv()
