import json
import os
import subprocess
import tempfile

from service.get_url_raw import get_gitlab_file_content
from utils.LogHandler import log
"""
调用Java命令，将Java文件转换为json

"""

def get_jar_file_path():
    """
    获取jar的位置
    """
    current_dir = os.getcwd()
    parent_dir = os.path.dirname(current_dir)
    jar_file_path = os.path.join(parent_dir, 'utils', 'javafilejson.jar')
    return jar_file_path


def execute_java_command(file_path):
    """
    执行Java命令
    file_path: Java文件路径
    """
    jar_file_path = get_jar_file_path()
    command = f'java -jar {jar_file_path} {file_path}'

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()

    if process.returncode == 0:
        print("命令执行成功！")
        print("输出：")
        all_data = output.decode("gbk")
        lst = json.loads(all_data)
        return lst
    else:
        print("命令执行失败！")
        print("错误信息：")
        print(error)


def process_java_file(project_id, file_path, version):
    """
    处理Java文件
    project_id: GitLab项目ID
    file_path: 文件路径
    version: 版本号
    """
    # 获取 文件的内容
    file_content = get_gitlab_file_content(project_id, file_path, version)

    # 创建临时文件
    with tempfile.NamedTemporaryFile(suffix='.java', delete=False, dir='.') as temp_file:
        # 获取临时文件路径
        temp_file_path = temp_file.name

        # 写入文件内容
        with open(temp_file_path, 'w', encoding="utf-8") as file:
            file.write(file_content)

        # 调用打印函数
        log.info(f"临时文件路径: {temp_file_path}")

        log.info(f"执行Java命令: java -jar javafilejson.jar {temp_file_path}")
        # 调用Java命令
        all_code = execute_java_command(temp_file_path)
        print(all_code)

    # 执行完后删除临时文件
    os.remove(temp_file_path)
    log.info(f"删除临时文件: {temp_file_path}")


if __name__ == '__main__':
    # 调用函数示例
    project_id = 755
    file_path = 'service/src/main/java/com/fujfu/flow/service/impl/api/FpPlatformServiceImpl.java'
    version = "master"
    process_java_file(project_id, file_path, version)
