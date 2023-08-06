from random import *
from time import *
import sys


def colour(l):
    if l == 0:
        sys.stdout.write("\033[97m")  # 白色
    if l == 1:
        sys.stdout.write("\033[90m")  # 黑色
    if l == 2:
        sys.stdout.write("\033[91m")  # 红色
    if l == 3:
        sys.stdout.write("\033[92m")  # 绿色
    if l == 4:
        sys.stdout.write("\033[93m")  # 黄色
    if l == 5:
        sys.stdout.write("\033[94m")  # 深蓝色
    if l == 6:
        sys.stdout.write("\033[95m")  # 紫色
    if l == 7:
        sys.stdout.write("\033[96m")  # 蓝色


def colour_r():
    # from random import *
    sj = randint(0, 7)
    if sj == 0:
        sys.stdout.write("\033[90m")  # 黑色
    if sj == 1:
        sys.stdout.write("\033[91m")  # 红色
    if sj == 2:
        sys.stdout.write("\033[92m")  # 绿色
    if sj == 3:
        sys.stdout.write("\033[93m")  # 黄色
    if sj == 4:
        sys.stdout.write("\033[94m")  # 深蓝色
    if sj == 5:
        sys.stdout.write("\033[95m")  # 紫色
    if sj == 6:
        sys.stdout.write("\033[96m")  # 蓝色
    if sj == 7:
        sys.stdout.write("\033[97m")  # 白色


def ColourPrint(a="", b=0.05, c=1, d=1.1):  # 内容，打印间隔时间，是(1)否(0)跳行，是(1)否(0)彩字.是(1)否(0)逐个彩字
    try:
        f = a + ""
    except:
        a = str(a)
    if d == 1.1:
        # print("\033[95m")
        colour_r()
        for u in a:
            sys.stdout.write(u)
            sys.stdout.flush()

            sleep(b)
            colour_r()
    elif d == 1:
        colour_r()
        for u in a:
            sys.stdout.write(u)
            sys.stdout.flush()
            sleep(b)
    else:
        for u in a:
            sys.stdout.write(u)
            sys.stdout.flush()
            sleep(b)
    if c == 1:
        print()