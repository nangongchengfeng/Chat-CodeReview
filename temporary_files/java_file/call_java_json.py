import json
import os
import subprocess
import tempfile

from temporary_files.java_file.get_url_raw import get_gitlab_file_content
from temporary_files.test import encode_file_path


def execute_java_command(file_path):
    """
    执行Java命令
    file_path: Java文件路径
    """

    command = f'java -jar javafilejson.jar {file_path}'

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()

    if process.returncode == 0:
        print("命令执行成功！")
        print("输出：")
        all_data = output.decode("gbk")
        lst = json.loads(all_data)
        for i in lst:
            print(i["name"])
    else:
        print("命令执行失败！")
        print("错误信息：")
        print(error)


def print_file_content(file_name):
    """
    打印文件内容
    """
    print(f"文件名: {file_name}")


def process_java_file(project_id, file_path, version):
    """
    处理Java文件
    project_id: GitLab项目ID
    file_path: 文件路径
    version: 版本号
    """

    file_content = get_gitlab_file_content(project_id, file_path, version)

    # 创建临时文件
    with tempfile.NamedTemporaryFile(suffix='.java', delete=False, dir='.') as temp_file:
        # 获取临时文件路径
        temp_file_path = temp_file.name

        # 写入文件内容
        with open(temp_file_path, 'w', encoding="utf-8") as file:
            file.write(file_content)

        # 调用打印函数
        print_file_content(temp_file_path)

        # 调用Java命令
        execute_java_command(temp_file_path)

    # 执行完后删除临时文件
    os.remove(temp_file_path)


if __name__ == '__main__':
    # 调用函数示例
    project_id = 755
    file_path = 'service/src/main/java/com/fujfu/flow/service/impl/api/FpPlatformServiceImpl.java'
    file_path = encode_file_path(file_path)
    version = "master"
    process_java_file(project_id, file_path, version)
