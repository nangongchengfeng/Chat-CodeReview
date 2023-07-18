# -*- coding: utf-8 -*-
# @Time    : 2023/7/7 21:03
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : deal_package.py.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
# @Time    : 2020/5/6 16:17
# @Author  : yu.lei

import os


def export_package():
    os.system("pipreqs ./ --encoding='utf-8' --force")


def input_package():
    os.system("pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple")


if __name__ == '__main__':
    export_package()