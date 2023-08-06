# @Time    : 2018/3/29 上午12:28
# @Author  : Niyoufa
import os

def traverse_tree(path, file_handle=None):
    """
    遍历文件目录
    :param path: 目录路径
    :param file_handle: 文件处理函数
    :return: None
    """
    if not os.path.abspath(path):
        raise Exception("path is not exists")

    for root, dirs, files in os.walk(path):
        print(root, dirs, files)
        if callable(file_handle):
            for file in files:
                file_handle(root, file)

if __name__ == "__main__":
    traverse_tree(".", file_handle=lambda x:print(x))