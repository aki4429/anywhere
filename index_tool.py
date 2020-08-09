#!/usr/bin/env python
# -*- coding: utf-8 -*-

#２次元配列の先頭行index取得(PO no. inv no. の位置)
def get_xindex(hyo, word):
    #print('hyo[0]', hyo[0])
    #print('word', word)
    return hyo[0].index(word)

#２次元配列の先頭列index取得(hcode の位置)
def get_yindex(hyo, word):
    for y, row in enumerate(hyo):
        if row[0] == word :
            return y



