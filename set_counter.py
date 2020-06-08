# vim:fileencoding=utf-8

"""
014CH271-37 と 014CH232W-37 を
ヌードボディーの発注から数えて
合計を返す。
"""

class SetCounter:
    def __init__(self):
        self.count ={}
        self.count['014CH232W-37'] = 0
        self.count['014CH271-37'] = 0
        self.count['014CH261-17B'] = 0

    def set(self, code:str, qty:int):
        if code == '014CH232W-03B':
            self.count['014CH232W-37'] += (2 * qty)
        #elif code == '014CH232W-37':
        #    self.count['014CH232W-37'] += (1 * qty)
        elif code == '014CH232W-06B':
            self.count['014CH232W-37'] += (1 * qty)
        elif code == '014CH232W-07B':
            self.count['014CH232W-37'] += ( 1 * qty)
        elif code == '014CH232W-08B':
            self.count['014CH232W-37'] += ( 1 * qty)
        elif code == '014CH232W-09B':
            self.count['014CH232W-37'] += ( 1 * qty)
        elif code == '014CH232W-20B':
            self.count['014CH232W-37'] += ( 1 * qty)
        elif code == '014CH232W-49B':
            self.count['014CH232W-37'] += ( 1 * qty)
        elif code == '014CH232W-50B':
            self.count['014CH232W-37'] += ( 1 * qty)
        #elif code == '014CH271-37':
        #    self.count['014CH271-37'] += ( 1 * qty)
        elif code == '014CH271E-03B':
            self.count['014CH271-37'] += ( 2 * qty)
        elif code == '014CH271E-08B':
            self.count['014CH271-37'] += ( 1 * qty)
        elif code == '014CH271E-09B':
            self.count['014CH271-37'] += ( 1 * qty)
        elif code == '014CH271E-41B':
            self.count['014CH271-37'] += ( 1 * qty)
        elif code == '014CH271E-42B':
            self.count['014CH271-37'] += ( 1 * qty)
        elif code == '014CH271E-49B':
            self.count['014CH271-37'] += ( 1 * qty)
        elif code == '014CH271E-50B':
            self.count['014CH271-37'] += ( 1 * qty)
        #elif code == '014CH261-17B':
        #    self.count['014CH261-17B'] += ( 1 * qty)
        elif code == '014CH261-03B':
            self.count['014CH261-17B'] += ( 1 * qty)



