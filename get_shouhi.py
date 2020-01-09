#!/usr/bin/env python
# -*- coding: utf-8 -*-

#オービックの在庫表から、発注検討表作成用に
#消費実績をとりだす。

import csv
import sqlite3
import os
import glob

from hin_slice import bunkai
from hinmoku_2 import Hinmoku

from index_tool import get_xindex, get_yindex

JDIR = './jisseki/*.csv'
NNAME = './zaiko_d/nunoji_hinban.csv'

def read_nunohin(filename):
    #オリジナル布地名と新コードのデータを読み込む
    data = []
    with open(filename, encoding='CP932') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)

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


def read_shouhi():
    filenames = glob.glob(JDIR)
    data=[]
    for filename in filenames:
        a= filename.split('-')
        month = a[0][-2:]+a[1][:2]
        with open(filename, 'r', encoding='CP932') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader: 
                if row[9] == "南濃倉庫" and row[11] == "通常":
                #品目コード6, 品目名7, 当月出庫18, 在庫場所 9, 在庫状態 11
                    if row[6].startswith('0') :
                        #商品コードが０で始まるものは材料なのでキーは品目コード
                        data.append([month, row[6], int(float(row[18]))])
                    else: 
                        #商品はキーは品目名
                        row[7] = rep_nuno(row[7]) #布地コード読替え
                        h = Hinmoku(bunkai(row[7]))
                        if not h.is_byorder():
                            data.append([month, h.make_code(), int(float(row[18]))])

    data.sort()
    return data

#data = read_nunohin(NNAME)

#data = read_shouhi()

def make_monthlist():
    files = os.listdir('jisseki')
    monthlist = []
    for f in files:
        monthlist.append( f.split('-')[0][-2:]+f.split('-')[1][:2])

    return monthlist

def make_shouhi(codelist):
    monthlist = make_monthlist()
    data = read_shouhi()

    #消費表用の2次元配列を初期化してデータを代入する
    shouhi_hyo = [['' for i in range(len(monthlist)+1)] for j in range(len(codelist)+1)]

    #codelist.insert(0, "") #先頭行はタイトル行なので空けておく
    #1列目にコードを代入
    for i, code in enumerate(codelist):
        shouhi_hyo[i+1][0] = code

    #１行目にmonthを代入
    for i, m in enumerate(monthlist):
        shouhi_hyo[0][i+1] = m

    for row in data: #month, コード、当月出庫
        if get_yindex(shouhi_hyo, row[1]) is not None \
                and get_xindex(shouhi_hyo, row[0]) is not None :
            shouhi_hyo[get_yindex(shouhi_hyo, row[1])][get_xindex(shouhi_hyo, row[0])] = row[2]

    with open('shouhi_hyo.csv', 'w', encoding='CP932') as f:
        writer = csv.writer(f)
        writer.writerows(shouhi_hyo)
        print('shouhi_hyo.csv を書きました。')

    return shouhi_hyo

#for row in data:
#    print(row[0], row[1], row[2])

#print(read_kh()[1])
#print(row[0], row[1])

