# -*- coding: utf-8 -*-
# @Time    : 2023/7/8 9:11
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : chat_test.py
# @Software: PyCharm
import os

import openai


def total_counts(response):
    # 计算本次任务花了多少钱和多少tokens：
    tokens_nums = int(response['usage']['total_tokens'])  # 计算一下token的消耗
    price = 0.002 / 1000  # 根据openai的美元报价算出的token美元单价
    人民币花费 = '{:.5f}'.format(price * tokens_nums * 7.5)
    合计内容 = f'本次对话共消耗了{tokens_nums}个token，花了{人民币花费}元（人民币）'
    print(合计内容)

    return float(人民币花费)


class Chat:
    def __init__(self, conversation_list=[]) -> None:
        # 初始化对话列表，可以加入一个key为system的字典，有助于形成更加个性化的回答
        # self.conversation_list = [{'role':'system','content':'你是一个非常友善的助手'}]
        self.conversation_list = []  # 初始化对话列表
        self.costs_list = []  # 初始化聊天开销列表

    # 打印对话
    def show_conversation(self, msg_list):
        for msg in msg_list[-2:]:
            if msg['role'] == 'user':  # 如果是用户的话
                # print(f"\U0001f47b: {msg['content']}\n")
                pass
            else:  # 如果是机器人的话
                message = msg['content']
                print(f"\U0001f47D: {message}\n")
            print()

    # 调用chatgpt，并计算开销
    def ask(self, prompt):
        self.conversation_list.append({"role": "user", "content": prompt})
        openai.api_key = 'sk-xxxx	'
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.conversation_list, temperature=0.5,
                                                # max_tokens=20,
                                                top_p=1, )
        print(response)
        answer = response.choices[0].message['content']
        # 下面这一步是把chatGPT的回答也添加到对话列表中，这样下一次问问题的时候就能形成上下文了
        self.conversation_list.append({"role": "assistant", "content": answer})
        # [{'role': 'user', 'content': '我叫王明瑶'}, {'role': 'assistant', 'content': '你好，王明瑶！有什么我可以帮助你的吗？'}, {'role': 'user', 'content': '我叫什么名字'}, {'role': 'assistant', 'content': '你的名字是王明瑶。'}]
        print(self.conversation_list)
        self.show_conversation(self.conversation_list)

        人民币花费 = total_counts(response)
        self.costs_list.append(人民币花费)
        print()


def main():
    talk = Chat()
    print()

    count = 0
    count_limit = eval(input("你想要对话的次数是多少呢？\n(请输入数字即可)"))
    while count < count_limit:  # 上下文token数量是有极限的，理论上只能支持有限轮次的对话，况且，钱花光了也就不能用了。。。
        if count < 1:
            words = input("请问有什么可以帮助你的呢？\n(请输入您的需求或问题)：")
        else:
            words = input("您还可以继续与我交流，请您继续说：\n(请输入您的需求或问题)：")
        print()
        talk.ask(words)
        count += 1

    print("对不起，您已达到使用次数的限额，欢迎您下次使用！")
    print(f'本轮聊天合计花费{sum(talk.costs_list)}元人民币。')


if __name__ == "__main__":
    os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
    os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"
    main()
