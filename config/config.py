# -*- coding: utf-8 -*-
# @Time    : 2023/7/7 21:28
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : config.py.py
# @Software: PyCharm
import platform


# openai-chatgpt 相关配置
model_quester_anster = "text-davinci-003"
model_gpt_35_turbo = "gpt-3.5-turbo"
model_programming_translate = "code-davinci-002"

sys_platform = platform.platform().lower()

# 错误类型
# 没有费用
ERROR_NO_FEE = {
    "error": 'You exceeded your current quota',
    "desc": "费用不足"
}
# 账号信息不对
ERROR_ACCOUNT_INFO = {
    "error": 'Incorrect API key provided',
    "desc": "账号API信息有误"
}
# 违法政策
ERROR_VIOLATION_POLICIES = {
    "error": 'Your access was terminated due to violation of our policies',
    "desc": "违反政策"
}

