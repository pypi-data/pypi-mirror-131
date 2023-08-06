# @Time    : 2018/3/29 上午12:14
# @Author  : Niyoufa
import os

def get_project_template_path():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "conf/project_template/project_name")

def get_module_template_path():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "conf/module_template/module_name")