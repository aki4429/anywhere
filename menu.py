#coding:utf-8

#TFC管理するためのメニュー

import write_zk
import juchu_reader
import edit_pd_code
import po_status
import inv_status
import os
import po_balance

MENU_TITLE = """-------------------------------
TFC管理メニュー
-------------------------------
"""

MENU = """1) 在庫表作成
2) バイオーダー発注
3) TFCコード
4) PO編集
5) invoice編集
  """   

class Menu:
    def __init__(self):
        num = self.sel()

    #メニューを表示して、選んだ番号を返す関数
    def sel(self):
        os.system('clear')
        ans = ""
        while ans != 'q' :
            print(MENU_TITLE)
            print(MENU)
            ans = input("編集する番号を選んでください(q=終了):")
            if ans != 'q' and ans.isdigit() :
                #num = int(ans) -1
                num = int(ans)
                self.go(num)

    def go(self, num):
        if num == 1:
            os.system('clear')
            print("手順(1) orbicから、仕入先コード:190001から190002までの手配表をO/P。")
            print("手順(2) 手配表をアップロードしてください。")
            po_balance.reset()
            write_zk.write_zk()
        elif num == 2:
            j = juchu_reader.JuchuReader()
        elif num == 3:
            e = edit_pd_code.EditPdCode()
        elif num == 4:
            p = po_status.PoStatus()
        elif num == 5:
            inv = inv_status.InvStatus()

        #elif num == 3:
            #t = tfc_edit_pd.Tfc




m = Menu()

