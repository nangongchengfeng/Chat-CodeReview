# -*- coding: utf-8 -*-
# @Time    : 2023/7/7 21:30
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : ai_code_review.py
# @Software: PyCharm
#https://xie.infoq.cn/article/f7009354c4875527b30330b92
import os

import gitlab
import openai


class AICodeReview():
    def __init__(self,
                 gitlab_private_token,
                 project_id,
                 merge_request_id,
                 openai_api_key,
                 gitlab_server_url='https://gitlab.ownit.top',
                 ):
        self.gl = gitlab.Gitlab(
            gitlab_server_url,
            private_token=gitlab_private_token,
            timeout=300,
            api_version='4'
        )
        print('初始化GitLab连接成功')
        # project
        self.project_id = project_id
        self.project = self.gl.projects.get(project_id)
        print('找到project')

        # mr
        self.merge_request_id = merge_request_id
        self.merge_request = self.project.mergerequests.get(merge_request_id)
        print('找到mr')

        # changes
        self.changes = self.merge_request.changes()
        # print(self.changes['changes'])
        # for change in self.changes['changes']:
        #     if any(ext in change['new_path'] for ext in ['py', 'java', 'class', 'vue']):
        #         print('找到变更文件')
        #         print(change['diff'])
        #         exit(1)
        #     else:
        #         print('变更文件不是代码文件')



        # commits
        # self.commits = self.project.commits.get('db0fc913')
        # print('找到commits')
        # print(self.commits)
        # print(self.commits.diff())

        # for commit in self.commits.diff():
        #     print(commit)

        # openai
        openai.api_key = openai_api_key

        # comments
        self.review_notes = []

        # note
        self.note = ''

    def ai_code_review(self):

        print('开始code review')
        for change in self.changes['changes']:
            print(change['diff'])
            if any(ext in change['new_path'] for ext in ['py', 'java', 'class', 'vue']):
            # https://platform.openai.com/docs/guides/chat/introduction
                messages = [
                    {"role": "system",
                     "content": "你是是一位资深编程专家，，正在进行 code review，这是一个 commit request，以格式「变更评分：实际的分数」给变更打分，分数区间为0~100分。这个变更的作用是什么? 这部分代码有问题吗? 如果有问题有没有更好的写法?\n\n\n新代码(import from 模块导入新代码不用显示)：\n${newCode} "
                     },
                    {"role": "user",
                     "content": f"请review这部分代码变更{change}",
                     },
                ]

                print('思考中...')
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                )
                new_path = change['new_path']
                print(f'对 {new_path} review中...')
                response_content = response['choices'][0]['message']['content'].replace('\n\n', '\n')
                total_tokens = response['usage']['total_tokens']

                review_note = f'# `{new_path}`' + '\n\n'
                review_note += f'({total_tokens} tokens) {"AI review 意见如下:"}' + '\n\n'
                review_note += response_content
                print(review_note)
                exit(1)
                self.review_notes.append(review_note)

if __name__ == '__main__':
