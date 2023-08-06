
入门示例
====

安装microserver
-------------
* git clone https://gitee.com/youfani/microserver.git
* cd microserver
* python setup.py install
* pip install -r requirements.txt

新建项目和模块
-------
* microserver-admin.py createproject myproject
* cd myproject
* python run.py createmodule mymodule

以下是在ubuntu16.04, python3.5.4 下的演示输出::

    aegis@Aegis123:~/test$ microserver-admin.py createproject myproject
    /home/aegis/anaconda3/lib/python3.5/site-packages/microserver-2.0.8-py3.5.egg/microserver/conf/project_template/project_name [] ['__init__.py-tpl', 'README.md-tpl', 'settings.py-tpl', 'run.py-tpl', 'requirements.txt-tpl']
    project myproject create success: /home/aegis/test/myproject
    aegis@Aegis123:~/test$ cd myproject/
    aegis@Aegis123:~/test/myproject$ python run.py createmodule mymodule
    /home/aegis/anaconda3/lib/python3.5/site-packages/microserver-2.0.8-py3.5.egg/microserver/conf/module_template/module_name [] ['__init__.py-tpl', 'handlers.py-tpl']
    module mymodule create success: /home/aegis/test/myproject/mymodule
    aegis@Aegis123:~/test/myproject$ tree
    .
    ├── __init__.py
    ├── mymodule
    │   ├── handlers.py
    │   └── __init__.py
    ├── README.md
    ├── requirements.txt
    ├── run.py
    └── settings.py

mymodule.handlers 代码如下::

    from tornado import gen

    from microserver.core.handlers import handlers
    from microserver.utils import decorator


    class MymoduleHandler(handlers.BaseHandler):

        @decorator.handler_except
        def prepare(self):
            """在请求方法 get、post等执行前调用，进行通用的参数初始化，支持协程"""
            pass

        @decorator.future_except
        @gen.coroutine
        def get(self, *args, **kwargs):
            """IO操作"""
            result = self.init_response_data()
            self.finish(result)

        @decorator.threadpoll_executor
        def post(self, *args, **kwargs):
            """耗时操作"""
            result = self.init_response_data()
            return result


    handlers = [
        (r"/mymodule", MymoduleHandler),
    ]

配置安装模块列表
--------
在settings.py文件中配安装模块列表MODULES字段，指向包含handlers的python模块::

    # 模块配置
    MODULES = [
        "mymodule.handlers",
    ]

启动web服务器
--------
* python run.py startserver 8087::

    aegis@Aegis123:~/test/myproject$ python run.py startserver 8087
    'mymodule.handlers'
    /mymodule
    ioloop
    ioloop
    ioloop
    ioloop
    server start, port: 8087!
    server start, port: 8087!
    server start, port: 8087!
    server start, port: 8087!
    ioloop
    ioloop
    server start, port: 8087!
    server start, port: 8087!
    ioloop
    ioloop
    server start, port: 8087!
    server start, port: 8087!

测试接口
----
使用python requests包调用接口::

    >>> import requests
    >>> requests.get("http://192.168.11.88:8087/mymodule").content.decode()
    '{"code": 200, "msg": "返回成功"}'
    >>>







