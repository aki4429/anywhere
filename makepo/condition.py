# -*- coding:utf-8 -*-

import csv
import os

#conditionsファイル(輸入条件)のデータを読んで操作するクラス。

class Condition:
    def __init__(self, name, shipment_per, shipto_1, shipto_2, shipto_3, shipto_4, shipto_5,via, forwarder, trade_term, payment, insurance, comment):
        self.line = []
        self.name = name
        self.shipment_per = shipment_per
        self.shipto_1 = shipto_1
        self.shipto_2 = shipto_2
        self.shipto_3 = shipto_3
        self.shipto_4 = shipto_4
        self.shipto_5 = shipto_5
        self.via = via
        self.forwarder = forwarder
        self.trade_term = trade_term
        self.payment = payment
        self.insurance = insurance
        self.comment = comment

        self.line.append(name)
        self.line.append(shipment_per)
        self.line.append(shipto_1)
        self.line.append(shipto_2)
        self.line.append(shipto_3)
        self.line.append(shipto_4)
        self.line.append(shipto_5)
        self.line.append(via)
        self.line.append(forwarder)
        self.line.append(trade_term)
        self.line.append(payment)
        self.line.append(insurance)
        self.line.append(comment)


    #表示用の関数
    def show(self):
        print("name:", self.name)
        print("shipment per:", self.shipment_per)
        print("ship to(1):", self.shipto_1)
        print("ship to(2):", self.shipto_2)
        print("ship to(3):", self.shipto_3)
        print("ship to(4):", self.shipto_4)
        print("ship to(5):", self.shipto_5)
        print("via:", self.via)
        print("forwarder:", self.forwarder)
        print("trade term:", self.trade_term)
        print("payment:", self.payment)
        print("insurance:", self.insurance)
        print("comment:", self.comment)

    #1行表示の文字列を返します。
    def make_line(self):
        l = "|".join(self.line)
        return l

    def show_line(self):
        print(self.make_line())



