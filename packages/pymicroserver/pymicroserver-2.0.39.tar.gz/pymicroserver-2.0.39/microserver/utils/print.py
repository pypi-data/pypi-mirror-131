# @Time    : 2018/3/28 下午8:47
# @Author  : Niyoufa


"""
格式：\033[显示方式;前景色;背景色m
 2
 3 说明：
 4 前景色            背景色           颜色
 5 ---------------------------------------
 6 30                40              黑色
 7 31                41              红色
 8 32                42              绿色
 9 33                43              黃色
10 34                44              蓝色
11 35                45              紫红色
12 36                46              青蓝色
13 37                47              白色
14 显示方式           意义
15 -------------------------
16 0                终端默认设置
17 1                高亮显示
18 4                使用下划线
19 5                闪烁
20 7                反白显示
21 8                不可见
"""
def error_print(info):
    print("\033[1;31;40m" + str(info) + "\033[0m")

def warning_print(info):
    print("\033[1;33;40m" + str(info) + "\033[0m")

def green_print(info):
    print("\033[1;32;40m" + str(info) + "\033[0m")

def format_print(obj):
    if isinstance(obj, dict):
        print("  {")
        for k, v in obj.items():
            print("    %s : %s"%(k, v))
        print("  }")
    elif isinstance(obj, list):
        print("[")
        for sub_obj in obj:
            format_print(sub_obj)
        print("]")
    else:
        print(obj)