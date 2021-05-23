#!/usr/bin/env python
# -*- coding: utf-8 -*-

#品目名を分解

HIN=slice(0,8) #品目CD
SHI=slice(8,11) #仕様
PIE=slice(11,17) #ピース
PAR=slice(17,20) #パーツ
IRO=slice(20,24) #色
NU1=slice(24,31) #布地1
NU2=slice(31,38) #布地2
TOK=slice(38,40) #特

class Hinmoku:
    def __init__(self, line):
        #品目コード全体から、各フィールドを取り出して格納する
        self.hin = line[0]
        self.shi = line[1]
        self.pie = line[2]
        self.par = line[3]
        self.iro = line[4]
        self.nu1 = line[5]
        self.nu2 = line[6]
        self.tok = line[7]
        #self.hin = line[HIN].replace(" ","") 
        #self.shi = line[SHI].replace(" ","") 
        #self.pie = line[PIE].replace(" ","") 
        #self.par = line[PAR].replace(" ","") 
        #self.iro = line[IRO].replace(" ","") 
        #self.nu1 = line[NU1].replace(" ","") 
        #self.nu2 = line[NU2].replace(" ","") 
        #self.tok = line[TOK].replace(" ","") 


    #藤栄モデルだったらTrue
    def is_fujiei(self):
        if self.hin.startswith('CH1021'):
            return True
        elif self.hin.startswith("IL714EO"):
            return True
        elif self.hin.startswith("IL715EO"):
            return True
        elif self.hin.startswith("CH931EO"):
            return True
        else:
            return False

    #完成品在庫モデルだったらTrue
    def is_kansei(self):
        if self.hin.startswith('CH271') and self.nu1=='SP/183':
            return True
        else:
            return False

    #バイオーダーの判定(Zがtok(特注)に含まれるか
    def is_byorder(self):
        if "Z" in self.tok:
            #print("tok", self.tok)
            return True
        else:
            #print("tok", self.tok)
            return False

    #次のコードは、TFCバイオーダーではないので除外
    def jogai(self):
        #次のコードで始まるものは除外
        if self.hin.startswith("BLS"):
            return True
        elif self.hin.startswith("BIVOS"):
            return True
        elif self.hin.startswith("BRU"):
            return True
        elif self.hin.startswith("CU"):
            return True
        elif self.hin.startswith("D528"):
            return True
        elif self.hin.startswith("F780"):
            return True
        elif self.hin.startswith("H287"):
            return True
        elif self.hin.startswith("N111"):
            return True
        elif self.hin.startswith("N264"):
            return True
        elif self.hin.startswith("N528"):
            return True
        elif self.hin.startswith("N666"):
            return True
        elif self.hin.startswith("P717"):
            return True
        elif self.hin.startswith("SDT005"):
            return True
        elif self.hin.startswith("SLT"):
            return True
        elif self.hin.startswith("T010"):
            return True
        elif self.hin.startswith("T323"):
            return True
        elif self.hin.startswith("T523"):
            return True
        elif self.hin.startswith("T565"):
            return True
        elif self.hin.startswith("TDS"):
            return True
        elif self.hin.startswith("X"):
            return True
        elif self.hin.startswith("Y436"):
            return True
        elif self.hin.startswith("Y714"):
            return True
        else:
            return False

    def make_code(self):
        #仕様のフィールドにNがあれば、品名の末尾にNを追加
        if "N" in self.shi :
            code = self.hin + "N"
        elif "E" in self.shi :
            code = self.hin + "E"
        else:
            code = self.hin

        #CH232N は CH232W に変換
        if code == "CH232N" :
            code = "CH232W"

        #CH232-35 は 新仕様と同じなので、CH232W-35 に変換
        if code == "CH232" and  "35" in self.pie:
            code = "CH232W"

        #CH232-37 は 新仕様と同じなので、CH232W-37 に変換
        if code == "CH232" and  "37" in self.pie:
            code = "CH232W"

        #CH1072はピースのSETを外す
        #if "CH1072" in self.hin :
        #    self.pie = self.pie.replace("SET", "")

        #CH271の、脚色DB/NAは外す
        if "CH271" in self.hin :
            self.iro = self.iro.replace("DB", "")
            self.iro = self.iro.replace("NA", "")

        #CH1071の、脚色NAはDBに変える
        if "CH1071" in self.hin :
            self.iro = self.iro.replace("NA", "DB")

        #CH1145 は 仕様に SS があれば、S SHがあれば、Hをつい生き
        if "CH1145" in self.hin :
            if "SS" in self.shi :
                code = self.hin + "S"
            elif "SH" in self.shi :
                code = self.hin + "H"

        #パーツフィールドに"C"があれば、ピース末尾にCをつける
        if "C" in self.par :
            piece = self.pie + "C "
            self.par = self.par.replace("C", "") #パーツのCは削除しておく
        else:
            piece = self.pie + " "

        #LH03 は、/の入っていない布地名の場合、布地名の末尾から３文字目に / を挿入
        if "LH03" in self.hin and not '/' in self.nu1:
            fab1 = self.nu1[:-2] + "/" + self.nu1[-2:]
        # CH1021は、布地名の末尾から３文字目に - を挿入
        elif "CH1021" in self.hin :
            fab1 = self.nu1[:-2] + "-" + self.nu1[-2:]
        else:
            fab1 = self.nu1

        #fabricが9053/9066で始まるものは、HSQをつける
        #fabricが9053は、末尾にZをつける
        if fab1.startswith("9053Z") :
            fab1 = fab1.replace("9053Z", "HSQ9053Z")
        elif fab1.startswith("9053") :
            fab1 = fab1.replace("9053", "HSQ9053Z")

        if fab1.startswith("9066") :
            fab1 = fab1.replace("9066", "HSQ9066")

        code_line = code + "-"
        code_line += piece 
        if len(self.par) != 0 :
            code_line += self.par + ""
        if len(self.iro) !=0  :
            code_line += self.iro + " " 
        if len(fab1) !=0  :
            code_line += fab1
        if len(self.nu2) !=0  :
            code_line += " " + self.nu2
        #if len(self.tok) !=0  :
        #    code_line += self.tok

        #CH271-08 /09 /49 /50 は CH271N
        #if "CH271-08 " in code_line:
        #    code_line = code_line.replace("CH271", "CH271N")
        #elif "CH271-09 " in code_line:
        #    code_line = code_line.replace("CH271", "CH271N")
        #elif "CH271-49 " in code_line:
        #    code_line = code_line.replace("CH271", "CH271N")
        #elif "CH271-50 " in code_line:
        #    code_line = code_line.replace("CH271", "CH271N")

        return code_line

    def print_detail(self):
        print("HIN:", self.hin)
        print("SHI:", self.shi)
        print("PIE:", self.pie)
        print("PAR:", self.par)
        print("IRO:", self.iro)
        print("NU1:", self.nu1)
        print("NU2:", self.nu2)
        print("TOK:", self.tok)

