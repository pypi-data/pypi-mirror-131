# @Time    : 2018/5/21 10:02
# @Author  : Niyoufa
from microserver.addons.swagger.api import SwaggerManager
from microserver.addons.swagger.handlers import SwaggerAPIDocHandler, SwaggerIOHandler, \
    SwaggerModuleIOHandler, SwaggerModuleAPIHandler

swagger_manager = SwaggerManager()
swagger_config = swagger_manager.get_swagger_config()
swagger_url = swagger_config.get("SWAGGER_URL") or "/swagger"
swagger_index_url = swagger_config.get("SWAGGER_INDEX_URL") or "/swagger/index.yml"

handlers = [
    (r"%s$"%swagger_url, SwaggerIOHandler),
    (r"%s$"%swagger_index_url, SwaggerAPIDocHandler),
    (r"%s/(?P<module>[0-9a-z_]+)$"%swagger_url, SwaggerModuleIOHandler),
    (r"%s/(?P<module>[0-9a-z_\.]+)$"%swagger_url, SwaggerModuleAPIHandler),
]