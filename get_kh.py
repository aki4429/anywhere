#!/usr/bin/env python
# -*- coding: utf-8 -*-

#オービックの発注検討表から在庫報告、発注検討表作成用に
#在庫と受注数をとりだす。

import csv
import sqlite3
import os
import glob

from hin_slice import bunkai
from hinmoku_2 import Hinmoku

KDIR = './kentohyo/*.csv'
NNAME = './zaiko_d/nunoji_hinban.csv'
CNAME = './zaiko_d/cover_zaiko.csv'

def read_nunohin(filename):
    #オリジナル布地名と新コードのデータを読み込む
    data = []
    with open(filename, encoding='CP932') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)

    return data

def read_cov(filename):
    #カバーデータファイルを読み込む
    data =[]
    with open(filename, 'r', encoding='CP932') as csvfile:
        reader = csv.reader(csvfile)
        #next(reader)
        for row in reader:
            data.append([row[0], int(row[1]),int(float(row[2]))])

    return data


def rep_nuno(code):
    #布オリジナル番号は読み替える
    nuno_data = read_nunohin(NNAME)
    for nuno in nuno_data:
        if nuno[0] in code:
            code = code.replace(nuno[0], nuno[1])

    return code

def sum_list(data):
    #コードが同じデータの在庫数と受注数を加算して一つにまとめる。
    code ={}  #キーをコード、値を在庫と受注のリスト[在庫,受注]の辞書
    c_data = [] #まとめたデータ保管用変数

    for row in data:
        code.setdefault(row[0], [0,0])
        code[row[0]] = [ x + y for (x,y) in zip(code[row[0]], [row[1], row[2]])]

    #辞書からリストに戻す
    for k, v in code.items():
        c_data.append([k] + v)

    return c_data


def read_kh():
    filename = glob.glob(KDIR)[-1]
    print(os.path.basename(filename), "を読み込みます。")
    covd =  read_cov(CNAME) #カバーデータを読み込む
    data = []
    with open(filename, 'r', encoding='CP932') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader: 
            #商品コード10, 規格12,現在在庫南濃倉庫-開始日以前出庫予定数,
            # 受注数-出庫予定数
            kijunbi = row[6] #基準日6を取り込み
            if row[10].startswith('0'):
                #商品コードが０で始まるものは材料なのでキーは商品コード
                if not row[10].startswith('0132'):
                    #ただし、0132で始まるカバーはロケーション管理のため除外
                    if row[10].startswith('013'):
                        #コード文字数制限で省略したCHを戻しておく
                        row[10] = row[10].replace('013', '013CH')

                data.append([row[10], int(float(row[17]))-int(float(row[20])),
                    int(float(row[126]))-int(float(row[20]))])
            elif not row[10].startswith('1'):
                #1で始まる余計な材料コードは除く
                row[12] = rep_nuno(row[12]) #布地コード読替え
                h = Hinmoku(bunkai(row[12]))
                if h.is_kansei() or not h.is_byorder():
                #if h.is_kansei() :
                    data.append([h.make_code(), int(float(row[17]))-int(float(row[20])),
                    int(float(row[126]))-int(float(row[20]))])

    data = data + covd
    data = sum_list(data)
    data.sort()
    return data, kijunbi

#data = read_nunohin(NNAME)

#data = read_kh()[0]
#data = read_kh()[0]
#data.sort()
#for row in data:
#    print(row[0], row[1], row[2])

#print(read_kh()[1])
#print(row[0], row[1])
data, kijunbi = read_kh()
#print('data', data)
print('kijunbi', kijunbi)
with open('kh_data.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(data)

