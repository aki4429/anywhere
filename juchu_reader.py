#!/usr/bin/env python
# -*- coding: utf-8 -*-

#受注実績表フォルダ読み込み、ファイル名を選択して
#juchu_read.py に渡す

import os
import juchu_read

class JuchuReader:
    def __init__(self):
        self.files = self.get_files()
        filename = self.files[-(self.sel_day())]
        print("filename:", filename)
        jr = juchu_read.JuchuRead(os.path.join("juchu", filename))
        jr.show()
        jr.show_ng()

    def get_files(self):
        files = os.listdir("juchu")
        files.sort()
        return files

    def sel_day(self):
        num = 1
        for i in range(-1, -7, -1):
            print(str(num) + ")" +self.files[i])
            num += 1

        print("-" * 10)
        bango = int(input("番号を選んでください:"))
        return bango

#j = JuchuReader()
