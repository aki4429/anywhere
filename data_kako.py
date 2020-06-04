#!/usr/bin/env python
# -*- coding: utf-8 -*-

# juchu_read のデータを受け取って、CH232, 271, 907などは、
# セットのクッションを減らし、LH03は、脚オーダーを追加する
# ための関数

#受注データ構造= 品目名,受注伝票№,受注日,納期,受注数

#条件によってデータ追加する。
def kako_add(data):
    new_list =[]
    for row in data:
        new_list.append(row)
        #CH232/CH271で背クッション付きは37をマイナス数量で追加
        if "CH232W-03 " in row[0]:
            new_list.append([row[0].replace("-03", "-37"), row[1], row[2],
                row[3], row[4] * -2])

        if "CH232W-06 " in row[0]:
            new_list.append([row[0].replace("-06", "-37"), row[1], row[2],
                row[3], row[4] * -1])

        if "CH232W-07 " in row[0]:
            new_list.append([row[0].replace("-07", "-37"), row[1], row[2],
                row[3], row[4] * -1])

        if "CH232W-08 " in row[0]:
            new_list.append([row[0].replace("-08", "-37"), row[1], row[2],
                row[3], row[4] * -1])

        if "CH232W-09 " in row[0]:
            new_list.append([row[0].replace("-09", "-37"), row[1], row[2],
                row[3], row[4] * -1])

        if "CH232W-20N " in row[0]:
            new_list.append([row[0].replace("-20N", "-37"), row[1], row[2],
                row[3], row[4] * -1])

        if "CH232W-49 " in row[0]:
            new_list.append([row[0].replace("-49", "-37"), row[1], row[2],
                row[3], row[4] * -1])

        if "CH232W-50 " in row[0]:
            new_list.append([row[0].replace("-50", "-37"), row[1], row[2],
                row[3], row[4] * -1])

        if "CH271-03 " in row[0]:
            new_list.append([row[0].replace("CH271-03", "CH271-37"),
                row[1], row[2], row[3], row[4] * -2])

        if "CH271N-08 " in row[0]:
            new_list.append([row[0].replace("CH271N-08", "CH271-37"),
                row[1], row[2], row[3], row[4] * -1])

        if "CH271N-09 " in row[0]:
            new_list.append([row[0].replace("CH271N-09", "CH271-37"),
                row[1], row[2], row[3], row[4] * -1])

        if "CH271N-49 " in row[0]:
            new_list.append([row[0].replace("CH271N-49", "CH271-37"),
                row[1], row[2], row[3], row[4] * -1])

        if "CH271N-50 " in row[0]:
            new_list.append([row[0].replace("CH271N-50", "CH271-37"),
                row[1], row[2], row[3], row[4] * -1])

        if "CH271-41 " in row[0]:
            new_list.append([row[0].replace("CH271-41", "CH271-37"),
                row[1], row[2], row[3], row[4] * -1])

        if "CH271-42 " in row[0]:
            new_list.append([row[0].replace("CH271-42", "CH271-37"),
                row[1], row[2], row[3], row[4] * -1])


        if "CH271E-03 " in row[0]:
            new_list.append([row[0].replace("CH271E-03", "CH271-37"),
                row[1], row[2], row[3], row[4] * -2])

        if "CH271E-08 " in row[0]:
            new_list.append([row[0].replace("CH271E-08", "CH271-37"),
                row[1], row[2], row[3], row[4] * -1])

        if "CH271E-09 " in row[0]:
            new_list.append([row[0].replace("CH271E-09", "CH271-37"),
                row[1], row[2], row[3], row[4] * -1])

        if "CH271E-49 " in row[0]:
            new_list.append([row[0].replace("CH271E-49", "CH271-37"),
                row[1], row[2], row[3], row[4] * -1])

        if "CH271E-50 " in row[0]:
            new_list.append([row[0].replace("CH271E-50", "CH271-37"),
                row[1], row[2], row[3], row[4] * -1])

        if "CH271E-41 " in row[0]:
            new_list.append([row[0].replace("CH271E-41", "CH271-37"),
                row[1], row[2], row[3], row[4] * -1])

        if "CH271E-42 " in row[0]:
            new_list.append([row[0].replace("CH271E-42", "CH271-37"),
                row[1], row[2], row[3], row[4] * -1])


        if "CH907-06 " in row[0]:
            new_list.append([row[0].replace("CH907-06", "CH907-35"),
                row[1], row[2], row[3], row[4] * -1])
            new_list.append([row[0].replace("CH907-06", "CH907-37"),
                row[1], row[2], row[3], row[4] * -1])

        if "CH907-07 " in row[0]:
            new_list.append([row[0].replace("CH907-07", "CH907-35"),
                row[1], row[2], row[3], row[4] * -1])
            new_list.append([row[0].replace("CH907-07", "CH907-37"),
                row[1], row[2], row[3], row[4] * -1])

        if "CH907-49 " in row[0]:
            new_list.append([row[0].replace("CH907-49", "CH907-35"),
                row[1], row[2], row[3], row[4] * -1])
            new_list.append([row[0].replace("CH907-49", "CH907-37"),
                row[1], row[2], row[3], row[4] * -1])

        if "CH907-50 " in row[0]:
            new_list.append([row[0].replace("CH907-50", "CH907-35"),
                row[1], row[2], row[3], row[4] * -1])
            new_list.append([row[0].replace("CH907-50", "CH907-37"),
                row[1], row[2], row[3], row[4] * -1])

        #CH907でコンビ布地の指定がない場合、おなじ布地名をコンビ名と
        #して追加。(ダブルでコードを選ばないように
        #ただし、35/37はそのまま。
        #if "CH907" in row[0]:
        #    if "CH907-35" not in row[0] and "CH907-37" not in row[0] and \
        #     "C " not in row[0]: 
        #        if len(row[0].split(" ")) < 3:
        #            row[0] = row[0] + " " + row[0].split(" ")[1]

        #CH261は、03を03+17コードに変換して、17をマイナス。
        #セットで注文くる前提の処理
        if "CH261-03 " in row[0]:
            new_list.append([row[0].replace("CH261-03", "CH261-17"),
                row[1], row[2], row[3], row[4] * -1])
            row[0] = row[0].replace("CH261-03", "CH261-03+17")

        if "LH03" in row[0]:
            #カバーは除く
            if "C" not in row[0]:
                #スツールはLEG=Sがつく
                if "-17 " in row[0]:
                    new_list.append(["LH03LEG-S",
                        row[1], row[2], row[3], row[4] * 1])
                elif "-17L " in row[0]:
                    new_list.append(["LH03LEG-S",
                        row[1], row[2], row[3], row[4] * 1])
                else:
                    new_list.append(["LH03LEG-L",
                        row[1], row[2], row[3], row[4] * 1])

    return new_list

#品目CD row[0] と 受注# row[1] が同じならば、数量row[4]を加算
def sum(data):
    #品番順受注番号順に並べ替え
    #data = sorted(data, key = lambda x:x[0])
    data = sorted(data, key = lambda x:x[1])
    #コードrow[0]+ 受注番号row[1] の辞書を作る
    new_dic = {}
    for row in data:
        #コードrow[0]+ 受注番号row[1] の組み合わせが辞書にあれば
        #データの数量を加算
        if row[0]+row[1] in new_dic:
            new_dic[row[0]+row[1]][4] += row[4]
        #無ければ、辞書にデータを登録
        else:
            new_dic[row[0]+row[1]] = row

    #辞書の値の取り出し。
    new_data =[]
    new_data = new_dic.values()

    del_list = []
    #数量0のデータを除外
    for row in new_data:
        if row[4] != 0:
            del_list.append(row)

    return del_list

def check(data, codes):
    new_data = []
    for row in data:
        flag="NO"
        idn=""
        for code in codes:
            #if row[0] in code[1] :
            if row[0] == code[1] :
                #print('row[0]', row[0])
                #print('code[1]', code[0], code[1])
                if flag == "NO":
                    flag = "ok"
                    idn = code[0]
                else:
                    flag = "Double"

        #obic_code を末尾に持っていきたいので、取り出しておく
        if len(row) > 5 :  #obic_code がある場合、データ帳は６になる。
            obic_code = row.pop()
        else:
            obic_code =''

        row.append(flag)
        row.append(idn)
        row.append(obic_code)


    return data
