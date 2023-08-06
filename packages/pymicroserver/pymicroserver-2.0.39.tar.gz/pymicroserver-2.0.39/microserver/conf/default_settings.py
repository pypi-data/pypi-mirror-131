# @Time    : 2018/4/8 17:43
# @Author  : Niyoufa
import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 服务器调试模式, 值为False时不自动重启服务器
DEBUG = False

# 变更自动重启
AUTORELOAD = False

# cookie secret key
COOKIE_SECRET = '{cookie_secret}'

# 是否开启csrf攻击防范
XSRF_COOKIES = False

# 允许访问的HOST配置
ALLOWED_HOSTS = []

# 模块配置
MODULES = [
    # "swagger",
]

# 命令配置
COMMANDS = []

# 数据库配置
DATABASES = {}

# 缓存
CACHES = {}

# 静态文件目录
STATIC = ""

# 模板文件目录
TEMPLATE = ""

# 算法模型目录
DATA = ""

PAGE_SIZE = 10

PAGE_SHOW = 10

# addons.swagger模块配置
# SWAGGER = dict(
#     SWAGGER_UI_ADDRESS = "http://petstore.swagger.io/", # swagger ui 访问地址
#     SWAGGER_URL = "/swagger",                           # 项目swagger接口文档访问路径
#     SWAGGER_INDEX_URL = "/swagger/index.yml",           # 项目swagger接口文档首页访问地址
#     SWAGGER_INDEX_FILENAME = "index.yml",               # 项目swagger接口文档首页文件名
#     SWAGGER_PROJECT_NAME = "测试项目",                   # 接口文档项目名称
#     SWAGGER_BASE_URL = "http://localhost:8069",         # 项目swagger接口文档访问地址
#     SWAGGER_MODULES = ["test1.testswagger"],                               # 项目swagger接口文档模块列表
# )