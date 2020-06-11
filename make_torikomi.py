# vim:fileencoding=utf-8

"""
DB のPOデータを指定し、podataフォルダの
取り込み元データ(PONO.csvファイル）を読み込み、
発注取込み用ファイルを吐き出す
"""

from po_status import PoStatus
import datetime
import calendar
import csv
import os

#固定定数のindex 書き出し
HK = 1 #ヘッダ発注区分のindex
JC = 5 #事業所コードのindex
TANTO = 10 #担当者コードのindex
TK = 53 #支払帳端区分のindex
MK = 194 #明細発注区分のindex
SAIKEN = 195 #債務科目区分のindex
ZK = 203 #税率区分のindex
KK = 214 #仮単価区分のindex

#固定定数の定数値を指定
HK_V = '1' #ヘッダ発注区分の値
JC_V = '100' #事業所コードの値
TANTO_V = 'B061' #担当者コードの値
TK_V = '1' #支払帳端区分の値
MK_V = '1' #明細発注区分の値
SAIKEN_V = '3100' #債務科目区分の値
ZK_V = '0' #税率区分の値
KK_V = '0' #仮単価区分の値

#固定定数項目に定数値を代入する関数
def put_const(line:list)->list:
    line[HK] = HK_V
    line[JC] = JC_V
    line[TANTO] = TANTO_V
    line[TK] = TK_V
    line[MK] = MK_V
    line[SAIKEN] = SAIKEN_V
    line[ZK] = ZK_V
    line[KK] = KK_V

    return line

#tfc固定定数のindex 書き出し
SHIIRE = 11 #仕入先コードのindex
SHIHARAI = 32 #支払先コードのindex
PAYHOW = 55 #支払方法コードのindex
UPRICE = 215 #仕入単価のindex

#固定定数の定数値を指定
SHIIRE_V = '190001' #仕入先コードの値
SHIHARAI_V = '190002' #支払先コードの値
PAYHOW_V = '2007' #支払方法コードの値
UPRICE_V = '0' #仕入単価の値

#TFC固定定数項目に定数値を代入
def put_tfcconst(line:list)->list:
    line[SHIIRE] = SHIIRE_V
    line[SHIHARAI] = SHIHARAI_V
    line[PAYHOW] = PAYHOW_V
    line[UPRICE] = UPRICE_V

    return line

#PO変数のindex 
PON = 0 #仮伝票番号のindex
PODATE = 6 #発注日のindex
ETD_1 = 7 #ヘッダ入荷予定日のindex
ETD_2 = 8 #ヘッダ仕入予定日のindex
ETD_3 = 9 #ヘッダ仕入先納品日のindex
PAYDAY = 54 #支払予定日のindex
METD_1 = 220 #明細入荷予定日のindex
METD_2 = 221 #明細仕入予定日のindex
METD_3 = 222 #明細仕入先納品日のindex

#PO データの取得
p = PoStatus()
podata = p.joho #id, pon pod, etd, delivery from po
pon_v = podata[1]
podate_v = podata[2].replace('-','/')
if podata[4] != None and podata[4] != '--':
    etd_v = podata[4].replace('-','/')
else:
    etd_v = podata[3].replace('-','/')

def monthend(datedata:str, daysafter:int)->str:
    dt = datetime.datetime.strptime(datedata, '%Y/%m/%d')
    dt = dt + datetime.timedelta(days=daysafter)
    dt = dt.replace(day=calendar.monthrange(dt.year, dt.month)[1])
    return dt.strftime('%Y/%m/%d')

def put_podata(line:list)->list:
    line[PON] =pon_v
    line[PODATE] = podate_v
    line[ETD_1] = etd_v
    line[ETD_2] = etd_v
    line[METD_3] = etd_v
    line[METD_1] = etd_v
    line[METD_2] = etd_v
    line[METD_3] = etd_v
    line[PAYDAY] = monthend(etd_v, 90)       #納入日の90日後の月末

    return line

#item変数のindex 
SOKO_1 = 125 #ヘッダ倉庫コードのindex
SOKO_2 = 196 #明細倉庫コードのindex
M_LINE = 193 #明細行番号のindex
U_LINE = 230 #内訳行番号のindex
CODE = 198 #商品コードのindex
QTY = 208 #明細数量のindex
U_QTY = 237 #内訳数量のindex
TEKIYO = 223 #明細摘要

#取込み用データ行を受け取り、row[5] = obic code
#が 0 から始まる場合は、材料なので、
#soko = 'A0Z001', POナンバー枝番1 とし、材料行カウント
#それ以外は、仕入れ品なので、 soko = 'A10000', PO枝番2とし
#仕入れ品行カウント

#材料の場合
def zai_val(line:list, row:list, zai_counter:int)->list:
    line[PON] = line[PON] + '-1'
    line[SOKO_1] = 'A0Z001'
    line[SOKO_2] = 'A0Z001'
    line[M_LINE] = zai_counter
    line[U_LINE] = zai_counter
    line[CODE] = row[5]
    line[QTY] = row[4]
    line[U_QTY] = row[4]
    line[TEKIYO] = row[1]
    return line

#仕入れ品の場合
def shi_val(line:list, row:list, shi_counter:int)->list:
    line[PON] = line[PON] + '-2'
    line[SOKO_1] = 'A10000'
    line[SOKO_2] = 'A10000'
    line[M_LINE] = shi_counter
    line[U_LINE] = shi_counter
    line[CODE] = row[5]
    line[QTY] = row[4]
    line[U_QTY] = row[4]
    line[TEKIYO] = row[1]
    return line

#ヘッダ読み込み
tori_data = []
with open('toreikomi_headder.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        tori_data.append(row)


#データ読み込み
filename = pon_v + '.csv'
fullname = os.path.join('./podata', filename)

def read_podata(fullname:str, pon_v:str)->list:
    if not os.path.isfile(fullname):
        print('{}のデータファイルがありません。'.format(pon_v))
    else:
        with open(fullname) as f:
            reader = csv.reader(f)
            zai_counter = 0
            shi_counter = 0
            for row in reader:
                #ラインを初期化しておく。
                tori_line = [''] * 238
                tori_line = put_const(tori_line)
                tori_line = put_tfcconst(tori_line)
                tori_line = put_podata(tori_line)
                if row[5].startswith('0'):
                    zai_counter += 1
                    tori_line = zai_val(tori_line, row, zai_counter)

                else:
                    shi_counter += 1
                    tori_line = shi_val(tori_line, row, shi_counter)

                tori_data.append(tori_line)

        return tori_data



tori_data = read_podata(fullname, pon_v)
#データ書き込み
outfile = pon_v + '_torikomi.csv'
fullout = os.path.join('./podata', outfile)
                    
with open(fullout, 'w', encoding='CP932') as f:
    writer = csv.writer(f)
    writer.writerows(tori_data)
    print("{}を書き込みました".format(fullout))

