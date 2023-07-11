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
        log.debug(f'操作类型：{object_kind}', f'操作信息：{gitlab_message}')
        verify_token = request.headers.get('X-Gitlab-Token')
        # 项目为commit时，才进行代码检查
        if verify_token == WEBHOOK_VERIFY_TOKEN and object_kind == 'push':
            # 验证通过，获取commit的信息
            print(gitlab_message)
            project_id = gitlab_message.get('project')['id']
            project_commit_id = gitlab_message.get('commits')
            commit_list = []
            for i in project_commit_id:
                commit_list.append(i['id'])
                log.info(f'项目id：{project_id}', f'commit_id：{commit_list}')
            print(project_id, commit_list)
            for i in commit_list:
                # 获取commit的变更文件
                web_url = f"https://gitlab.fujfu.com/api/v4/projects/{project_id}/repository/commits/{i}/diff"
                print(web_url)
            return jsonify({'status': 'success'}), 200

        else:
            print('项目不是push')
            return jsonify({'status': 'bad token'}), 401

    else:
        abort(400)
