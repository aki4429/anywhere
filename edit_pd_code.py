# -*- coding:utf-8 -*-

import sqlite3
import code
import csv
import readline
import pandas as pd
from pandas import DataFrame, Series

FILEN = "tfc.sqlite"
FABLIST = "fab.csv"
#FILEN = "//172.16.161.24/生産管理部/TFCDB/tfc.sqlite"
OUTFILE = "po_lines_keep.csv"

MENU="(e)編集/(d)削除/(c)コピー・編集/(s)布地展開(クローン作成)/(p)発注リストに追加/(q)編集中止"

class EditSqlcode:
    def __init__(self):
        #DataFrame の表示拡大
        pd.set_option('display.max_columns', 100)
        #sqlite3データベース接続
        self.con = sqlite3.connect(FILEN)
        #self.cur = self.con.cursor()
        self.fablist = self.read_fab()
        self.id_list = []
        self.df = pd.read_sql_query("select * from tfc_code", con=self.con, index_col = 'id' )
        self.menu()
        self.df.to_sql("tfc_code", self.con, if_exists ="replace")
        self.con.close()

    #コード編集用メニューを起動
    def menu(self):
        moji = ""
        while(moji != 'q'):
            #self.df = pd.read_sql_query("select * from tfc_code", con=self.con, index_col = 'id' )
            ans = ''
            #print("=========検索メニュー=========")
            moji = input("検索文字を入力してください。(終了=q):")
            while moji != 'q' and ans != 'q':
                kekka = self.get_kekka(moji)
                if len(kekka) > 0 :
                    ans = self.edit_kekka(kekka)
                else:
                    ans = 'q'
                #print("ans", ans)

        print("検索メニューを終了します。")


    #検索文字の検索結果を表示
    def get_kekka(self, moji):
        self.id_list = []
        #print("get_kekkaしました。")
        #input()
        kekka = self.df[self.df.hinban.str.contains(moji)]
        if len(kekka) == 0:
            print("検索結果はゼロでした。")
            return []
        else:
            j = 0
            for i, row in kekka.iterrows():
                print(str(j+1)+")", *row, ":",i)
                self.id_list.append(i)
                j+=1

            #print('self.idlist', self.id_list)
            return kekka
            #return self.show_kekka(kekka)

    #検索結果のidリストから、idを選んで編集
    def edit_kekka(self, kekka):
        ans = input("編集する番号を選んでください(q=終了):")
        if ans != 'q' and ans.isdigit() :
            #idナンバー
            idn = self.id_list[int(ans)-1]
            code = self.df.loc[idn]
            print(code)
            print("-"*40)
            print(MENU)
            resp = input("編集内容を選んでください。")
            if resp == 'e':
                self.update_each(idn)
                self.df.to_sql("tfc_code", self.con, if_exists ="replace")

            elif resp == 'd':
                delcode = self.df.loc[idn].copy()
                self.df.drop(idn, inplace=True)
                print(delcode, "を削除しました。")
                #self.df.to_sql("tfc_code", self.con, if_exists ="replace")

            elif resp == 'c':
                #index の最大値+1
                newid = self.df.index[-1] + 1
                #追加indexに行追加して編集
                self.df.loc[newid] = self.df.loc[idn]
                self.update_each(newid)
                self.df.to_sql("tfc_code", self.con, if_exists ="replace")
                
            elif resp == 's':
                #new id はindex の最大値+1
                newid = self.df.index[-1] + 1
                #ファブリック名のcsv読み込み
                fl = pd.read_csv(FABLIST)

                #指定データからファブリック取り出し。
                #スペースでスプリット２番めの要素を切り出し。
                hinban = self.df.loc[idn].hinban
                spl = hinban.split(' ')
                #print('spl', spl)
                if len(spl) >1 :
                    fabcode = spl[len(spl)-1]
                
                #布地番号の色識別数字を除いて取り出し。
                preword = fabcode[:len(fabcode)-1]
                #print('preword', preword)
                #flistにファブリックコードグループを登録
                flist =[]
                for code in fl['fabcode'].values:
                    if code.startswith(preword) :
                        flist.append(code)

                print('flist', flist)
                #ファブコードグループの品番がDBにあるか確認して
                #無ければ、登録リストに追加
                addlist = []
                for fcode in flist:
                    new_hinban = hinban.replace(fabcode, fcode)
                    if len(self.df[self.df['hinban'] == new_hinban]) == 0:
                        print(new_hinban, "を登録しますか")
                        a = self.df.loc[idn].copy()
                        a['hinban'] = a['hinban'].replace(fabcode, fcode)
                        a['item']=a['item'].replace(fabcode, fcode)
                        a['description']=a['description'].replace(fabcode, fcode)
                        if a['hcode'] :
                            a['hcode'] = a['hcode'].replace(fabcode, fcode)
                        addlist.append(a)

                #print('addlist', addlist)
                kotae = input("はい/いいえ:(y/n)")
                i = 0
                if kotae == 'y':
                    for ad in addlist :
                        self.df.loc[newid + i] = ad
                        i += 1

                #追加indexに行追加して編集
                #self.df.loc[newid] = self.df.loc[idn]
                #self.update_each(newid)
                #self.df.to_sql("tfc_code", self.con, if_exists ="replace")
                
            elif resp == 'p':
                qty = input("発注数量を入力してください。:")
                om = input("受注番号をを入力してください。:")
                self.write_poline(OUTFILE, self.fablist, om, qty, code, idn)

        return ans

    def write_poline(self, filename, fablist, om, qty, code, idn):
        print('code', code)
        poline = []
        poline.append(code['hinban']) #品番
        poline.append(code['item']) #item
        poline.append(code['description']) #description
        poline.append(code['remarks']) #remark
        poline.append(qty)
        poline.append(code['unit']) #unit
        poline.append(code['uprice']) #u.price
        poline.append("")
        poline.append("")
        poline.append(self.make_our_item(fablist, code['hinban']))
        poline.append("")
        poline.append(om)
        poline.append("")
        poline.append(code['vol']) #vol
        poline.append(idn) #id
        #self.show_poline(poline)
        #print(poline)
        self.save_poline(filename, poline)


    #id番号を受け取って、カラム名毎に更新内容取得してUPDATE
    def update_each(self, idn):
        ans = ""
        while(ans != 'q'): 
            #指定されたindexのデータを変数に格納
            kekka = self.df.loc[idn]
            print(kekka)
            num = 1
            #カラム名(kekka=Series.index)に番号つけて選びやすく
            colnames ={}
            for k in kekka.index:
                print(str(num) + ") " + str(k) +":" + str(kekka[k]))
                colnames[num]=k
                num += 1

            ans = input("編集する番号を選んでください。終了=q:")
            if ans != 'q' and ans.isdigit() :
                #選択絡むの値をreadline の履歴に登録します。
                print("kekka", self.df.loc[idn, colnames[int(ans)]])
                if int(ans) <12 :
                    readline.add_history(self.df.loc[idn, colnames[int(ans)]])

                newdata = input("新しい内容を入力してください。:")
                self.df.loc[idn, colnames[int(ans)]] = newdata

                ans=""


    #検索結果を表示して、検索結果のidのリストを返す
    def show_kekka(self, kekka):
        ids = [] #id番号を格納するリスト
        num = 1 #行数表示用変数
        for k in kekka:
            line = ""
            line += str(num) + ") "
            line += str(k[1]) + "|"
            line += str(k[2]) + "|"
            line += str(k[3]) + "|"
            line += str(k[4]) + "|"
            line += str(k[5]) + "|"
            line += str(k[6]) + "|"
            line += str(k[7]) + "|"
            line += str(k[8]) 

            print(line)
            ids.append(k[0])
            num += 1

        return ids

    # ファブリック変換用ファイルを開く
    def read_fab(self):
        data = []
        with open("hukla_tfc_fab.csv", "r") as fl:
        #リストに読み込み
            reader = csv.reader(fl)
            for row in reader:
                data.append(row)
        
        return data

    def save_poline(self, filename, poline):
        # 書き出し用のファイルを開く
        with open(filename, "a", encoding="CP932") as out_file:
            writer = csv.writer(out_file,lineterminator='\n')
            writer.writerow(poline)

    def make_our_item(self, fablist, hinban):
        our_item = hinban
        for fline in fablist:
            our_item = our_item.replace(fline[0], fline[0] + "[" + fline[1] + "]")
        
        return our_item
   
e = EditSqlcode()
