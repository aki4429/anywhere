# -*- coding:utf-8 -*-

import csv
import copy
import readline

#コードの各項目の値を辞書形式でもつクラス。
#編集、表示、検索結果を返す

#FILEOUT = "//172.16.161.24/生産管理部/★★TFC保存★★/PO作成/po_lines.csv"
#FILEOUT = "po_lines.csv"
#FILEOUT = "po_lines_keep.csv"

class Code:
    def __init__(self, hinban, item, description, remarks, unit, u_price, our_item, u_M3, hcode):
        self.fields={}
        self.fields["品番"] = hinban
        self.fields["item"] = item
        self.fields["description"] = description
        self.fields["remarks"] = remarks
        self.fields["unit"] = unit
        self.fields["u_price"] = u_price
        self.fields["our_item"] = our_item
        self.fields["M3"] = u_M3
        self.fields["hcode"] = hcode

    #1行表示用の関数
    def show_line(self):
        print(self.line())

    def get_hinban(self):
        return self.fields["品番"]

    #1行表示の文字列を返します。
    def line(self):
        l = "|".join(self.fields.values())
        return l

    #番号)項目名:値で縦に表示
    def show_detail(self):
        i = 0
        print("-" * 20)
        for k, v in self.fields.items():
            print(str(i+1) + ")" + k + ": " + v)
            i += 1

        print("-" * 20)

    def edit(self):
        #コードのキー項目をリストにしておきます。
        articles = list(self.fields.keys())
        num = ""
        while num != 'q':
            #詳細表示します
            self.show_detail()
            #編集したい項目を選びます。
            num = input("編集したい項目を選んでください:(q=終了)")
            if num.isdigit():
                #キー項目名を取得します。
                k = articles[int(num)-1]
                #キー項目の値を取得します。
                v = self.fields[k]
                #readlline の履歴に登録します。
                readline.add_history(v)
                #項目の値を編集します。
                self.fields[k] = input(k + " の値を入力してください:")

    def search(self, moji):
        for v in self.fields.values():
            if moji in v:
                return True

        return False

    def __lt__(self, other):
        # self < other
        return self.fields["品番"] < other.fields["品番"]

    def list_exp(self):
        return list(self.fields.values())

    def make_poline(self, filename, fablist):
        ans = ""
        while ans != "y" and ans != 'q':
            qty = ""
            om = ""
            poline = []
            qty = input("発注数量を入力してください。")
            om = input("受注ナンバーを入力してください。")
            poline.append(self.fields["品番"])
            poline.append(self.fields["item"])
            poline.append(self.fields["description"])
            poline.append(self.fields["remarks"])
            poline.append(qty)
            poline.append(self.fields["unit"])
            poline.append(self.fields["u_price"])
            poline.append("")
            poline.append("")
            poline.append(self.make_our_item(fablist))
            poline.append("")
            poline.append(om)
            poline.append("")
            poline.append(self.fields["M3"])
            self.show_poline(poline)
            ans = input("これでよいですか。(よい=y, やめる=q):")

        if ans == 'y':
            self.save_poline(filename, poline)

    def make_our_item(self, fablist):
        our_item = copy.deepcopy(self.fields["品番"])
        for fline in fablist:
             our_item = our_item.replace(fline[0], fline[0] + "[" + fline[1] + "]")

        return our_item

    def show_poline(self, poline):
        print("品番:", poline[0])
        print("item:", poline[1])
        print("description:", poline[2])
        print("remarks:", poline[3])
        print("qty:", poline[4])
        print("unit:", poline[5])
        print("u.price:", poline[6])
        print("price:", poline[7])
        print("b:", poline[8])
        print("our item#:", poline[9])
        print("M3:", poline[10])
        print("OM:", poline[11])
        print("品種:", poline[12])
        print("u.M3:", poline[13])

    def write_poline(self, filename, fablist, om, qty):
        poline = []
        poline.append(self.fields["品番"])
        poline.append(self.fields["item"])
        poline.append(self.fields["description"])
        poline.append(self.fields["remarks"])
        poline.append(qty)
        poline.append(self.fields["unit"])
        poline.append(self.fields["u_price"])
        poline.append("")
        poline.append("")
        poline.append(self.make_our_item(fablist))
        poline.append("")
        poline.append(om)
        poline.append("")
        poline.append(self.fields["M3"])
        self.show_poline(poline)
        self.save_poline(filename, poline)

    def save_poline(self, filename, poline):
        # 書き出し用のファイルを開く
        with open(filename, "a", encoding="CP932") as out_file:
            writer = csv.writer(out_file,lineterminator='\n')
            writer.writerow(poline)

