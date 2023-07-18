# -*- coding: utf-8 -*-
# @Time    : 2023/7/13 17:39
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : get_url_raw.py
# @Software: PyCharm
import os
import tempfile
import urllib.parse

import requests

from config.apollo_config import gitlab_private_token, gitlab_server_url
from utils.LogHandler import log


def encode_file_path(file_path):
    """
    对文件路径进行URL编码
    """
    encoded_file_path = urllib.parse.quote(file_path, safe='')
    return encoded_file_path


def get_gitlab_file_content(project_id, file_path, version):
    """
    获取GitLab项目中指定文件的内容
    """
    headers = {
        'PRIVATE-TOKEN': gitlab_private_token  # 替换为你的访问令牌
    }

    url = f'{gitlab_server_url}/api/v4/projects/{project_id}/repository/files/{file_path}/raw?ref={version}'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        log.info(f'{url} API请求成功：{response.status_code} {response.reason}')
        file_content = response.text
        return file_content
    else:
        log.error(f'{url} API请求失败：{response.status_code} {response.reason}')
        return None


if __name__ == '__main__':
    # 调用函数示例
    project_id = 755
    file_path = 'service/src/main/java/com/fujfu/flow/service/impl/HandleMidServiceImpl.java'
    file_path = encode_file_path(file_path)
    version = "master"

    file_content = get_gitlab_file_content(project_id, file_path, version)
