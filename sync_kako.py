# vim:fileencoding=utf-8

"""
kako*.csv ファイルからSYNCするファイルを選んで、
読み込み、jucナンバーを取得
torikomi*.csv ファイルの同一juc行のみ残す。
"""

import select_file
import csv

#同期する加工ファイルを選びます。
filename = select_file.select_file('kako', '.', 'csv')

#加工ファイルを読んで、受注NO.リスト(row[1])のユニークリスト
with open(filename, encoding='CP932') as f:
#with open(filename) as f:
    reader = csv.reader(f)
    jucs = []
    for row in reader:
        jucs.append(row[1])

    jucs = set(jucs)

#動悸する発注取込みデータリストを選びます。
targetfile = select_file.select_file('torikomi', '.', 'csv')

#取込みリストを読みます。
#受注ナンバーがあれば、データを抽出します。
#その際、カウンターで数えて、受注NOが全部あるか
#確認します。
counter = 0
with open(targetfile, encoding='CP932') as f:
#with open(targetfile) as f:
    reader = csv.reader(f)
    sync_list = []
    for row in reader:
        for juc in jucs:
            on_off_setter = 'off'
            if row[1] == juc:
                sync_list.append(row)
                if on_off_setter == 'off':
                    counter += 1
                    on_off_setter == 'on'

if counter < len(jucs) :
    print('ターゲットファイルに受注No.が足りません。')

else:
    print('ターゲットファイルから抽出したデータを\
            torikomi_result.csv として保存します。')

with open('torikomi_result.csv', 'w', encoding='CP932') as f:
    writer = csv.writer(f)
    writer.writerows(sync_list)




