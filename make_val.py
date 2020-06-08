# vim:fileencoding=utf-8 

"""
発注取込み成功ファイルから、必要な値や
設定を書き出すためのプログラム
Python スクリプトの変数に使用するため
"""

import csv

FILENAME='torikomi_val.csv'

#読み込みます。
data = [] #name,index,項目,値,固定値
with open(FILENAME) as f:
    reader = csv.reader(f)
    headder = next(reader) #ヘッダ行はスキップ
    for row in reader:
        data.append(row)

#print(data)
#固定値の定数を取り出します。
kotei = []
for d in data:
    if int(d[4]) == 1: #固定値の定数は1を指定してあります。
        kotei.append(d)

#print(kotei)

#固定定数のindex 書き出し
print("#固定定数のindex 書き出し")
for d in kotei:
    print(d[0],"=", d[1], "#" + d[2] +"のindex")

#固定定数の定数値を指定
print("#固定定数の定数値を指定")
for d in kotei:
    print(d[0]+"_V", "=", "'"+d[3]+"'", "#" +d[2] + "の値")

#固定定数項目に定数値を代入
print("#固定定数項目に定数値を代入")
print("def put_const(data):")
print("for line in data:")
for d in kotei:
    print("line["+d[0]+"]", "=", d[0]+"_V")

#TFC固定値の定数を取り出します。
tfc = []
for d in data:
    if int(d[4]) == 2: #TFC固定値の定数は2を指定してあります。
        tfc.append(d)

#tfc固定定数のindex 書き出し
print("#tfc固定定数のindex 書き出し")
for d in tfc:
    print(d[0],"=", d[1], "#" + d[2] +"のindex")

#tfc固定定数の定数値を指定
print("#固定定数の定数値を指定")
for d in tfc:
    print(d[0]+"_V", "=", "'"+d[3]+"'", "#" +d[2] + "の値")

#固定定数項目に定数値を代入
print("#TFC固定定数項目に定数値を代入")
print("def put_tfcconst(data):")
print("for line in data:")
for d in tfc:
    print("line["+d[0]+"]", "=", d[0]+"_V")

#変数の項目を取り出します。
hensuu = []
for d in data:
    if int(d[4]) == 0: #変数の項目は0を指定してあります。
        hensuu.append(d)

#変数ののindex 書き出し
print("#変数のindex 書き出し")
for d in hensuu:
    print(d[0],"=", d[1], "#" + d[2] +"のindex")

