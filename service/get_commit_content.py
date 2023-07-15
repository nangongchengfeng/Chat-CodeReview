# -*- coding: utf-8 -*-
# @Time    : 2023/7/14 11:01
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : get_commit_content.py
# @Software: PyCharm

import requests

from config.apollo_config import gitlab_server_url, gitlab_private_token
from service.call_java_json import process_java_file
from utils.LogHandler import log


def get_commit_content(project_id, version, commit_id):
    headers = {
        "PRIVATE-TOKEN": gitlab_private_token,
    }

    if commit_id:
        for commit in commit_id:
            log.info(f"开始获取commit_id的路径: {commit}")
            file_dir = []
            url = f'{gitlab_server_url}/api/v4/projects/{project_id}/repository/commits/{commit}/diff'
            log.info(f"{commit}  开始请求gitlab的 {url} ，commit: {commit_id}的路径")
            response = requests.get(url, headers=headers)
            if response.status_code == 200:

                content = response.json()
                # 开始处理请求的内容
                log.info(f"开始处理请求的内容: {content}")
                for i in content:
                    file_dir.append(i['new_path'])
                    process_java_file(project_id, i['new_path'], version)
                log.info(f"数量： {len(file_dir)}  获取到的文件路径: {file_dir}")
    else:
        return []

if __name__ == "__main__":

    # 调用函数示例
    project_id = 798
    version = "dev"
    commit_id = ['d8f3dda9b233224edcd61c46f97391fb3b53dd42']

    file_dir = get_commit_content(project_id, version, commit_id)
