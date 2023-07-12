# -*- coding: utf-8 -*-
# @Time    : 2023/7/10 11:00
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : conmit_list.py
# @Software: PyCharm

import json

# 读取文件内容
with open('commit.txt', 'r', encoding='utf-8') as file:
    data = file.read()

# 现在`json_data`是一个JSON对象，您可以根据需要对其进行处理
json_data = eval(data)
commit_list=[]
commit_all=json_data['commits']
for i in commit_all:
    print(i)
    commit_list.append(i['id'])
print(commit_list)
