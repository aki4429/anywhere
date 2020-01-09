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

def bunkai(line):
    hin = line[HIN].strip()
    shi = line[SHI].strip()
    pie = line[PIE].strip()
    par = line[PAR].strip()
    iro = line[IRO].strip()
    nu1 = line[NU1].strip()
    nu2 = line[NU2].strip()
    tok = line[TOK].strip()

    return [hin, shi, pie, par, iro, nu1, nu2, tok]
