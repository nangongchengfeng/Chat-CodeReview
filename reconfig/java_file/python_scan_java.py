# -*- coding: utf-8 -*-
# @Time    : 2023/7/12 14:47
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : python_scan_java.py
# @Software: PyCharm
import javalang
from javalang import parse
from javalang.tree import MethodDeclaration

# from javaparser import parse as jp_parse


# 解析 Java 文件，生成 AST 语法树
file_path = "LoanInfoController.java"
with open(file_path, "r", encoding="utf-8") as f:
    file_content = f.read()
tree = parse.parse(file_content)

# 包名
print("package:")
print(tree.package.name)
print("######################################")

# 依赖
print("imports:")
for i in tree.imports:
    print(str(i.path))

print("######################################")
# 方法名
print("方法名：" + tree.types[0].methods[0].name)
print("方法修饰符：" + str(tree.types[0].methods[1].modifiers))
print("第一入参名：" + str(tree.types[0].methods[1].parameters[0].name))
print("第一入参类型：" + str(tree.types[0].methods[1].parameters[0].type.name))
print("返回值类型：" + str(tree.types[0].methods[1].return_type.name))
print("######################################")
# 提取所有方法
all_class_list= []
# 提取所有方法
for _, method_node in tree.filter(javalang.tree.MethodDeclaration):
    # 计算开始行
    start_line = method_node.position.line - 1  # javalang uses 1-based indexing
    print(start_line)
    # 提取方法体中的最后一个元素的结束行
    if method_node.body:

        last_statement = method_node.body[-1]
        print(last_statement)

        end_line = last_statement.position.line + 1 + len(str(last_statement).split('\n'))

        print(end_line)
        exit(1)
    else:  # 如果方法体为空，那么开始行和结束行相同
        end_line = start_line

    # 提取源代码
    method_source = file_content.split('\n')[start_line:end_line]
    # print('\n'.join(method_source))
    print("######################################")
    all_class_list.append(method_source)

# for i in all_class_list:
#     print(i)
#     print("######################################")