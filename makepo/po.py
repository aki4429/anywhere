# -*- coding:utf-8 -*-

import csv
import os
import condition

#POに関連するデータをもつクラス

class Po:
    def __init__(self, condition, podate, etddate, pono ) :
        self.condition = condition
        self.podate = podate
        self.etddate = etddate
        self.pono = pono



