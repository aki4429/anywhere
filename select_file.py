# vim:fileencoding=utf-8

import glob
import os


"""
文字を含むファイルを表示し、
そこから、ファイルを選ばせ、
ファイル名を返す関数
"""
def select_file(moji:str, folder:str, surfix:str)->str:
    letters = '*' + moji + '*' + '.' + surfix
    filelist = glob.glob(os.path.join(folder, letters))
    for i, n in enumerate(filelist):
        print(i+1, n)

    ans = input('ファイルを番号で選んでください。')
    filename = filelist[int(ans)-1]
    print(filename, 'が選ばれました。')

    return filename


