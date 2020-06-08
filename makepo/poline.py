# -*- coding:utf-8 -*-

import csv
import os

#po_line.csvファイルの項目を取り込み操作するクラス。

class Poline:
    def __init__(self, hinban, item, description, remarks, qty, unit, u_price, b_1, b_2,our_item, b_3, om, b_4, u_M3, code_id = 0, obic =''):
        self.line = []

        self.item = item
        self.description = description
        self.remarks = remarks
        self.qty = qty
        self.unit = unit
        self.u_price = u_price
        self.our_item = our_item
        self.om = om
        self.u_M3 = u_M3
        self.code_id = code_id

        self.line.append(item)
        self.line.append(description)
        self.line.append(remarks)
        self.line.append(qty)
        self.line.append(unit)
        self.line.append(u_price)
        self.line.append(our_item)
        self.line.append(om)
        self.line.append(u_M3)
        self.line.append(code_id)

    #1行表示用の関数
    def show_line(self):
        print(self.make_line())

    #1行表示の文字列を返します。
    def make_line(self):
        l = "|".join(self.line)
        return l

