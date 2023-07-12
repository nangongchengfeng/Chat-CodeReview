# -*- coding: utf-8 -*-
# @Time    : 2023/7/10 11:34
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : chat-review.py
# @Software: PyCharm
import os
import openai
import requests
from openai import OpenAIError
from retrying import retry
from utils.LogHandler import log
from config.apollo_config import gitlab_server_url, gitlab_private_token, openai_api_key, cookie

# 配置openai
openai_api_key = openai_api_key
gitlab_private_token = gitlab_private_token
Cookie = cookie
headers = {
    "PRIVATE-TOKEN": gitlab_private_token,
    "Cookie": Cookie
}


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
        log.info(f"创建评论成功，评论id: {comment_data}")
    else:
        log.error(f"请求失败，状态码: {response.status_code}")


def wait_and_retry(exception):
    return isinstance(exception, OpenAIError)


@retry(retry_on_exception=wait_and_retry, stop_max_attempt_number=3, wait_fixed=60000)
def generate_review_note(change):
    openai.api_key = openai_api_key
    messages = [
        {"role": "system",
         "content": "你是是一位资深编程专家，gitlab的commit代码变更将以git diff 字符串的形式提供，注意：代码中：- 表示删除的代码，+ 表示新增的代码 # 表示代码注释，以格式「变更评分：实际的分数」给变更打分，分数区间为0~100分。输出格式：然后，以精炼的语言、严厉的语气指出存在的问题。如果你觉得必要的情况下，可直接给出修改后的内容。你的反馈内容必须使用严谨的markdown格式。"
         },
        {"role": "user",
         "content": f"请review这部分代码变更{change['diff']}",
         },
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    new_path = change['new_path']
    log.info(f'对 {new_path} review中...')
    response_content = response['choices'][0]['message']['content'].replace('\n\n', '\n')
    total_tokens = response['usage']['total_tokens']
    review_note = f'### `{new_path}`' + '\n\n'
    review_note += f'({total_tokens} tokens) {"AI review 意见如下:"}' + '\n\n'
    review_note += response_content
    log.info(f'对 {new_path} review结束')
    return review_note


def chat_review(project_id, project_commit_id, content):
    log.info('开始code review')
    for change in content:
        log.info(f"单项目的commit内容： {change}")
        if any(ext in change['new_path'] for ext in ['py', 'java', 'class', 'vue']):
            try:
                review_note = generate_review_note(change)
                log.info(f'对 {change["new_path"]}  , review结果如下：{review_note}')
                post_comments(project_id, project_commit_id, review_note)
            except Exception as e:
                log.error(f'出现异常，异常信息：{e}')
        else:
            log.error(f'格式不正确，对 {change["new_path"]}  , 不需要review')


@retry(stop_max_attempt_number=3, wait_fixed=2000)
def review_code(project_id, project_commit_id):
    for commit_id in project_commit_id:
        url = f'https://gitlab.fujfu.com/api/v4/projects/{project_id}/repository/commits/{commit_id}/diff'
        log.info(f"开始请求gitlab的{url}   ,commit: {commit_id}的diff内容")

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            content = response.json()
            # 开始处理请求的类容
            log.info(f"开始处理All请求的类容: {content}")
            chat_review(project_id, commit_id, content)
        else:
            log.error(f"请求gitlab的{url}commit失败，状态码：{response.status_code}")
            raise Exception(f"请求gitlab的{url}commit失败，状态码：{response.status_code}")


if __name__ == '__main__':
    project_id = 190
    project_commit_id = ['7014a11ccd6e33c938616e6cac17b9cbe523d496']
    # os.environ["HTTP_PROXY"] = "http://192.168.96.19:7890"
    # os.environ["HTTPS_PROXY"] = "http://192.168.96.19:7890"
    log.info(f"项目id: {project_id}，commit_id: {project_commit_id} 开始进行ChatGPT代码补丁审查")
    review_code(project_id, project_commit_id)
    # post_comments(data)
