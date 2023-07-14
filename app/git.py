# -*- coding: utf-8 -*-
# @Time    : 2023/7/7 21:22
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : git.py
# @Software: PyCharm
import json
import subprocess
from os import abort

from flask import Blueprint, request, jsonify

from config.apollo_config import gitlab_server_url
from utils.LogHandler import log

git = Blueprint('git', __name__)


@git.route('/api')
def question():
    return 'hello world'


WEBHOOK_VERIFY_TOKEN = "asdhiqbryuwfqodwgeayrgfbsifbd"


@git.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        verify_token = request.headers.get('X-Gitlab-Token')
        if verify_token == WEBHOOK_VERIFY_TOKEN:
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'bad token'}), 401

    elif request.method == 'POST':
        gitlab_message = request.data.decode('utf-8')
        gitlab_message = json.loads(gitlab_message)
        object_kind = gitlab_message.get('object_kind')
        verify_token = request.headers.get('X-Gitlab-Token')
        # 项目为commit时，才进行代码检查
        if verify_token == WEBHOOK_VERIFY_TOKEN and object_kind == 'push':
            # 验证通过，获取commit的信息
            print(gitlab_message)
            # 获取项目id
            project_id = gitlab_message.get('project')['id']
            # 获取所有的commit的id
            project_commit_id = gitlab_message.get('commits')
            # 获取项目的分支
            version = gitlab_message.get('project')['default_branch']

            # 定义一个空列表，用来存放commit的id
            commit_list = []

            # 定义一个空列表，用来存放commit的url
            commit_list_url = []

            # 遍历commit的id
            for i in project_commit_id:
                commit_list.append(i['id'])
                commit_list_url.append(i['url'])

            print(project_id, version, commit_list)
            print(commit_list_url)

            for i in commit_list:
                # 获取commit的变更文件
                web_url = f"{gitlab_server_url}/api/v4/projects/{project_id}/repository/commits/{i}/diff"
                print(web_url)

            return jsonify({'status': 'success'}), 200

        else:
            print('项目不是push')
            return jsonify({'status': 'bad token'}), 401

    else:
        abort(400)
