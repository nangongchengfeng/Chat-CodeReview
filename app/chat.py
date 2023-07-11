# -*- coding: utf-8 -*-
# @Time    : 2023/7/7 21:22
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : chat.py
# @Software: PyCharm
from os import abort

from flask import Blueprint, request, jsonify

from utils.LogHandler import log


chat = Blueprint('chat', __name__)


@chat.route('/api')
def question():
    return 'hello world'

