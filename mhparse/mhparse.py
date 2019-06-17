# coding:utf-8

# [01/18(金)]形式の文字を日付けデータにパースする。

import datetime

yobi = ["月", "火", "水", "木", "金", "土", "日"]

# hiduke = '01/15(水)'


def parse(hiduke: str) -> datetime.date:
    """[01/18(金)]形式の文字を日付けデータにパースする。"""
    # 今年は?
    this_year = datetime.date.today().year

    # [/]で分割して、左側が月
    m = int(hiduke.split("/")[0])
    # print('m=', m)

    # [/]右を[(]で分割して左側が日
    d = int(hiduke.split("/")[1].split('(')[0])
    # print('d=', d)

    # [(]の右側が曜日、[)]を除去
    y = (hiduke.split("/")[1].split('('))[1].replace(')', '')
    # print(y)

    # 去年とすると
    t1 = datetime.date(this_year-1, m, d)
    # 今年とすると
    t2 = datetime.date(this_year, m, d)
    # 来年とすると
    t3 = datetime.date(this_year+1, m, d)

    # 曜日で判定する。
    if yobi[t1.weekday()] == y:
        return t1
    elif yobi[t2.weekday()] == y:
        return t2
    elif yobi[t3.weekday()] == y:
        return t3
    else:
        print("1年前後でその日付と曜日の組み合わせはありません。")


# result = parse(hiduke)

# print(result)
