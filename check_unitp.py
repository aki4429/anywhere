#!/usr/bin/env python
# -*- coding: utf-8 -*-

#インボイスを読み込んで、コード、品名、単価のデータを
#はき出す

import csv
import xlrd
import re
import sqlite3

#file_name = "//172.16.161.24/生産管理部/★★TFC保存★★/単価チェック/TI190117B_FUGUE.xls"

file_name = "./tanka/TI190629C_FUGUE.xls"
#file_name = "./tanka/TI190622C_TFC+SIC.xls"
#file_name = "./tanka/TI190615D_CH907.xls"
#file_name = "./tanka/TI190601D_FUGUE_Revised.xls"
#file_name = "./tanka/TI190525C_HAKATA.xls"
#file_name = "./tanka/TI190326C_TF1089.xls"

result_filename = file_name.replace("xls", "result.csv")

#FILEN = "//172.16.161.24/生産管理部/★★TFC保存★★/PO作成/tfc_code.csv"
#file_name = "TI181227B_FUGUE.xls"
#FILEN = "tfc/tfc_code.csv"
SFILE = "tfc.sqlite"

#インボスナンバー位置は0から数えて何行何列め？
#行
INV_ROW = 2
#列
INV_COL = 0

#０から数えてデータが始まる行
BEGIN_ROW = 12

#コード、品名、単価はゼロから数えて左から何列目？
CODE_COL = 1
NAME_COL = 2
UP_COL = 4
#UP_COL = 5

SHEET_NAME = "INVOCE"

print(file_name)

book = xlrd.open_workbook(file_name)
print(book.sheet_names())

sheet_name = SHEET_NAME

data = []

sheet = book.sheet_by_name(sheet_name)

#インボイス名取り出し
inv = sheet.cell(INV_ROW, INV_COL).value

#単価項目確認
upname = sheet.cell(BEGIN_ROW-1, UP_COL).value
print("upname=", upname)
if upname == "UNIT":
    up_col = UP_COL + 1
else:
    up_col = UP_COL


for row_index in range(BEGIN_ROW, sheet.nrows):
    code = sheet.cell(row_index, CODE_COL).value
    name = sheet.cell(row_index, NAME_COL).value
    uprice = sheet.cell(row_index, up_col).value
    if len(code) != 0 :
        data.append([name, code, uprice])


#for row in data:
#    print(row[0], row[1], row[2])

master = []
#コードファイル読み込んで、csvリスト(master) に格納
# 編集したいファイル（元ファイル）を開く
#with open(FILEN, "r", encoding="CP932") as f:
#with open(FILEN, "r") as f:
#    reader = csv.reader(f)
    # ファイルのヘッダーをnext メソッドで１行飛ばす
#    next(reader)
    # Codeクラスを生成して格納
#    for row in reader:
#        #品番、アイテム、uprice
#        master.append([row[0], row[1], row[5]]) 

#sqlite3からとりこみ
con = sqlite3.connect(SFILE)
cur = con.cursor()
cur.execute("select hinban, item, uprice from tfc_code")
master = cur.fetchall()
con.close()

#for cd in master:
#    print(cd)

def check(name, up, master):
    num_reg = re.compile("^\d+(\.\d+)?\Z")
    for row in master:
        #print("row[1]", row[1])
        #print("row[2]", type(row[2]))
        if row[1] == name:
            if num_reg.match(str(row[2])):
                if float(up) == float(row[2]):
                    return "ok"
                else:
                    return float(row[2])

    return "x"


for row in data:
    print(row[0], row[1], row[2], check(row[0], row[2], master))

with open(result_filename, "w", encoding="CP932") as w:
#with open("check_result.csv", "w", encoding="CP932") as w:
    writer = csv.writer(w)
    for row in data:
        line =[ row[0], row[1], row[2], check(row[0], row[2], master) ]
        writer.writerow(line)

    print(result_filename, "に書き込みました。")
