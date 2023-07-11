# -*- coding: utf-8 -*-
# @Time    : 2023/7/10 11:34
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : chat-review.py
# @Software: PyCharm
import os
# 测试： https://gitlab.fujfu.com/hxgroup/fujfu_member/-/commit/37cbe4f291c5e545d6830fe9273f53c26a2f2cfe
import openai
import requests
from retrying import retry

from utils.LogHandler import log
openai_api_key = os.getenv("OPENAI_API_KEY")
gitlab_private_token = os.getenv("GITLAB_PRIVATE_TOKEN")
Cookie = os.getenv("Cookie")
# url = 'https://gitlab.fujfu.com/api/v4/projects/124/repository/commits/37cbe4f291c5e545d6830fe9273f53c26a2f2cfe/diff'
# comments_url = 'https://gitlab.fujfu.com/api/v4/projects/124/repository/commits/37cbe4f291c5e545d6830fe9273f53c26a2f2cfe/comments'

headers = {
    "PRIVATE-TOKEN": gitlab_private_token,
    "Cookie": Cookie
}


#

@retry(stop_max_attempt_number=3, wait_fixed=2000)
def post_comments(id, commit_id, content):
    data = {
        'note': content
    }
    comments_url = f'https://gitlab.fujfu.com/api/v4/projects/{id}/repository/commits/{commit_id}/comments'
    response = requests.post(comments_url, headers=headers, json=data)
    log.debug(f"请求结果: {response.json}")
    if response.status_code == 201:
        comment_data = response.json()
        # 处理创建的评论数据
        print(comment_data)
    else:
        print(f"请求失败，状态码: {response.status_code}")


def chat_review(project_id, project_commit_id, content):
    openai.api_key = openai_api_key
    review_notes = []
    log.info('开始code review')
    for change in content:
        log.info(f"commit {change}")
        # print(change['new_path'])

        if any(ext in change['new_path'] for ext in ['py', 'java', 'class', 'vue']):
            messages = [
                {"role": "system",
                 "content": "你是是一位资深编程专家，代码变更将以git diff 字符串的形式提供：[代码中：- 表示删除的代码，+ 表示新增的代码 # 表示代码注释]，以格式「变更评分：实际的分数」给变更打分，分数区间为0~100分。输出格式：然后，以精炼的语言、严厉的语气指出存在的问题。如果你觉得必要的情况下，可直接给出修改后的内容。你的反馈内容必须使用严谨的markdown格式。"
                 },
                {"role": "user",
                 "content": f"请review这部分代码变更{change}",
                 },
            ]

            log.info('思考中...')
            # 加一个异常处理，如果限速了，就等待一段时间，在重试 直到接口返回结果为200
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                )
                new_path = change['new_path']
                print(f'对 {new_path} review中...')
                log.info(f'对 {new_path} review中...')
                # 获取返回的内容
                response_content = response['choices'][0]['message']['content'].replace('\n\n', '\n')
                # 获取返回的分数
                total_tokens = response['usage']['total_tokens']

                # 生成review的内容
                review_note = f'### `{new_path}`' + '\n\n'
                review_note += f'({total_tokens} tokens) {"AI review 意见如下:"}' + '\n\n'
                review_note += response_content
                log.info(f'对 {new_path} review结束')
                log.info(f'对 {new_path} review结果如下：{review_note}')

                # 开始提交评论
                post_comments(project_id, project_commit_id, review_note)
                # print(review_note)
                review_notes.append(review_note)
            except Exception as e:
                log.error(f'出现异常，异常信息：{e}')
    print(review_notes)





@retry(stop_max_attempt_number=3, wait_fixed=2000)
def review_code(project_id, project_commit_id):
    for commit_id in project_commit_id:
        url = f'https://gitlab.fujfu.com/api/v4/projects/{project_id}/repository/commits/{commit_id}/diff'
        print(url)
        log.info(f"开始请求gitlab的commit: {commit_id}的diff内容")
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            content = response.json()
            # 开始处理请求的类容
            print(content)
            log.info(f"开始处理请求的类容: {content}")
            chat_review(project_id, commit_id, content)
        else:
            print('请求失败')


if __name__ == '__main__':
    project_id = 124
    project_commit_id = ['37cbe4f291c5e545d6830fe9273f53c26a2f2cfe']
    # os.environ["HTTP_PROXY"] = "http://192.168.96.19:7890"
    # os.environ["HTTPS_PROXY"] = "http://192.168.96.19:7890"
    review_code(project_id, project_commit_id)
    # post_comments(data)
