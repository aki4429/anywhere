#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#在庫報告/発注検討表を作成するプログラム。

MENU ="""
作成する表を選んでください。
===========================
1) TFC在庫表
2) TFC検討表
--------------------------
番号で選んでください。(1/2/.. or q=終了): """

ZEXCEL = 'TFC_zaiko.xlsx'
KEXCEL = 'TFC_kento_template2.xlsx'

import openpyxl
import csv

from get_code import get_k, get_z, ori_sort
from get_kh import read_kh
from make_balance import MakeBalance
from index_tool import get_xindex, get_yindex

import get_shouhi_new
import get_shouhi

def join_data(c_data, k_data):
    #同じコードのコードデータに検討表データを繋ぐ(左結合)
    jdata = []
    for c_row in c_data:
        c_row = list(c_row)
        flag = 0
        for k_row in k_data:
            if c_row[0] == k_row[0]:
                c_row = c_row + k_row[1:]
                flag = 1

        if flag == 0:
            #同じコードが無い場合、在庫、受注数は0にしておく。
            c_row = c_row + [0,0]

        jdata.append(c_row)

    return jdata

def make_hyo(nolist, codelist, totallist):
    l = len(codelist[0])
    hyo = [['' for i in range(len(nolist)+l)] for j in range(len(codelist)+3)]
    #print('hyo', hyo)
    #先頭列にコードデータを代入
    for i, code in enumerate(codelist):
        hyo[i+3][:0] = code

    #print('hyo_withcode', hyo)
    #１行目にINV no. PO no. を代入
    for i, num in enumerate(nolist):
        hyo[0][i+l] = num[2]

    #2行目にetd を代入
    for i, num in enumerate(nolist):
        hyo[1][i+l] = num[1]

    #3行目にdelivery を代入
    for i, num in enumerate(nolist):
        hyo[2][i+l] = num[0]

    #print('hyo_final', hyo)
    with open('hyo_final.csv', 'w', encoding='CP932') as f:
        writer = csv.writer(f)
        writer.writerows(hyo)

    print('hyo_final.csv を書き出しました。')

    for row in totallist: #着日, etd, PO No. コード　残数
        yindex = get_yindex(hyo, row[3])
        #print('row[3]=', row[3], row[0], row[1], row[2], row[4], yindex)
        #if yindex == 0:
            #print('yindex0=', row[3], row[0], row[1], row[2], row[4])

        if yindex != None and yindex > 2: #yindex 行が 0-2 はタイトル行なので飛ばす。
            #print('index', yindex, row[2], row[4])
            hyo[yindex][get_xindex(hyo, row[2])] = row[4]

        elif yindex != None and yindex < 3:
            print('yindex_<3', yindex, row[2], row[4])


    return hyo

def write_zexcel(hyo, kijunbi, nolist):
    wb = openpyxl.load_workbook(ZEXCEL)
    sheet = wb['zaiko']
    sheet['C1'] = kijunbi

    #1行目にinv no, po no 記入
    n = 0 #7列目からスタート
    while n < len(nolist) :
        sheet.cell(row=1, column=n+7, value = nolist[n][2]) #po no.
        sheet.cell(row=2, column=n+7, value = nolist[n][1][5:]) #ETD
        sheet.cell(row=3, column=n+7, value = nolist[n][0][5:]) #delivery
        n += 1
    

    #コード他記入
    j=0
    i=4 #4行目からスタート
    while i < len(hyo):
        sheet.cell(row=i, column=2, value = hyo[i-1][0]) #コード
        sheet.cell(row=i, column=3, value = hyo[i-1][2]) #在庫
        sheet.cell(row=i, column=4, value = hyo[i-1][3]) #受注
        sheet.cell(row=i, column=5, value = '=C{0}-D{0}'.format(i)) #有効残
        sheet.cell(row=i, column=6, value = hyo[i-1][1]) #カテゴリー
        #入荷予定記入
        k = 4
        while k < len(hyo[0]): 
            sheet.cell(row=i, column=k+3, value = hyo[i-1][k])
            k+=1
        i += 1
        j += 1

    save_file = 'zaikohyo/N_TFC_zaiko_{0}.xlsx'.format(kijunbi.replace('/', '-'))
    wb.save(save_file)
    print("{}を保存しました。".format(save_file))

def write_kexcel(hyo, kijunbi, nolist):
    wb = openpyxl.load_workbook(KEXCEL)
    sheet = wb['kento']
    sheet['D2'] = kijunbi

    #2行目にinv no, po no 記入
    n = 0 #9列目からスタート
    while n < len(nolist) :
        sheet.cell(row=2, column=n+11, value = nolist[n][2]) #po no.
        sheet.cell(row=3, column=n+11, value = nolist[n][1][5:]) #ETD
        sheet.cell(row=4, column=n+11, value = nolist[n][0][5:]) #delivery
        n += 1
    

    #コード他記入
    j=0
    i=4 #5行目からスタート
    while i < len(hyo):
        sheet.cell(row=i+1, column=2, value = hyo[i-1][0]) #コード
        sheet.cell(row=i+1, column=5, value = hyo[i-1][3]) #在庫
        sheet.cell(row=i+1, column=6, value = hyo[i-1][4]) #受注
        sheet.cell(row=i+1, column=7, value = '=E{0}-F{0}'.format(i+1)) #有効残
        sheet.cell(row=i+1, column=1, value = hyo[i-1][2]) #カテゴリー
        sheet.cell(row=i+1, column=4, value = hyo[i-1][1]) #容積
        #入荷予定記入
        k = 5
        while k < len(hyo[0]): 
            sheet.cell(row=i+1, column=k+6, value = hyo[i-1][k])
            k+=1
        i += 1
        j += 1

    
    sheet2 = wb['jisseki']
    #コード他記入(実績シートに)
    #コードリスト取り出し
    codelist = []
    for i, row in enumerate(hyo):
        if i >2 :
            codelist.append(row[0])

    #消費実績表作成 

    #obic 旧データの消費実績取り出し
    shouhi_hyo_old = get_shouhi.make_shouhi(codelist)
    #obic 新データの消費実績取り出し
    shouhi_hyo_new = get_shouhi_new.make_shouhi(codelist)

    #それぞれのヘッダ行を取り出して
    h_o = shouhi_hyo_old.pop(0)
    h_n = shouhi_hyo_new.pop(0)
    h_line = h_o + h_n[1:] #ヘッダを結合しておく 

    #旧消費データ(2次元配列)の品名が同じ新消費データのデータを
    #つなげて shouhi_hyo に代入。
    shouhi_hyo = []

    for row_o in shouhi_hyo_old:
        for row_n in shouhi_hyo_new:
            if row_o[0] == row_n[0] :
                shouhi_hyo.append(row_o + row_n[1:])

    #さっきのヘッダを1行目に置く。
    shouhi_hyo.insert(0, h_line)

    i=0 #1行目からスタート
    ylength = len(shouhi_hyo)
    xlength = len(shouhi_hyo[0])
    while i < ylength:
        j=0 #1列目からスタート
        while j < xlength :
            sheet2.cell(row=i+1, column=j+1, value = shouhi_hyo[i][j])
            j += 1
        i += 1

    save_file = 'zaikohyo/TFC_kento_{0}.xlsx'.format(kijunbi.replace('/', '-'))
    wb.save(save_file)
    print("{}を保存しました。".format(save_file))

def write_zk():

    data = read_kh()
    k_data =  data[0]
    kijunbi = data[1]
    mb = MakeBalance()
    nolist = mb.make_nolist()

    ans = ''
    while ans != 'q':
        ans = input(MENU)
        #検討表から在庫と受注数をとりだす。
        if ans == '1':
            print("在庫表を作成します")
            #在庫コードデータを取り出し。
            c_data = ori_sort(get_z())
            zdata=join_data(c_data, k_data)
            #旧モデルで在庫と受注の無いものは省きます。
            zdata = [e for e in zdata if not (e[1] == '旧モデル' and e[2] == 0 and e[3] == 0)]
            #print('mb', mb.totallist)
            #print('nolist', nolist)
            hyo = make_hyo(nolist, zdata, mb.totallist)
            write_zexcel(hyo, kijunbi, nolist)
        
            with open('zdata.csv', 'w', encoding='CP932') as f:
                writer = csv.writer(f)
                writer.writerows(hyo)

        elif ans == '2':
            print("検討表を作成します")
            c_data = ori_sort(get_k())
            kdata=join_data(c_data, k_data)
            hyo = make_hyo(nolist, kdata, mb.totallist)
            write_kexcel(hyo, kijunbi, nolist)

            with open('kdata.csv', 'w', encoding='CP932') as f:
                writer = csv.writer(f)
                writer.writerows(hyo)


