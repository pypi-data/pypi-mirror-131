# @Time    : 2018/5/21 10:03
# @Author  : Niyoufa
# @Time    : 2018/5/18 14:08
# @Author  : Niyoufa
from microserver.core.handlers import handlers
from microserver.addons.swagger.api import SwaggerManager

from microserver.addons.swagger.template_loader import SwaggerYmlLoader


class SwaggerIOHandler(handlers.NoAuthHandler):

    def get(self, *args, **kwargs):
        swagger_manager = SwaggerManager()
        swagger_config = swagger_manager.get_swagger_config()
        swagger_index_url = swagger_config.get("SWAGGER_INDEX_URL") or "/swagger/index.yml"
        swagger_ui_address = swagger_config.get("SWAGGER_UI_ADDRESS") or "http://petstore.swagger.io/"

        index_url = "%s://%s%s"%(self.request.protocol, self.request.host, swagger_index_url)
        self.redirect("%s?url=%s"%(swagger_ui_address, index_url))


class SwaggerAPIDocHandler(handlers.NoAuthHandler):

    def get(self, *args, **kwargs):
        self.set_header("Access-Control-Allow-Origin", "*")

        swagger_manager = SwaggerManager()

        try:
            swagger_manager.create_apidoc()
        except Exception as err:
            print(err.args)

        swagger_index_filename = swagger_manager.swagger_config.get("SWAGGER_INDEX_FILENAME") or "index.yml"
        self.render(swagger_index_filename)


class SwaggerModuleIOHandler(handlers.NoAuthHandler):

    def get(self, *args, **kwargs):
        swagger_manager = SwaggerManager()
        swagger_config = swagger_manager.get_swagger_config()
        swagger_ui_address = swagger_config.get("SWAGGER_UI_ADDRESS") or "http://petstore.swagger.io/"
        module_url = "%s://%s%s"%(self.request.protocol, self.request.host, self.request.path + ".yml")
        self.redirect("%s?url=%s"%(swagger_ui_address, module_url))


class SwaggerModuleAPIHandler(handlers.NoAuthHandler):

    def get(self, *args, **kwargs):
        self.set_header("Access-Control-Allow-Origin", "*")

        swagger_manager = SwaggerManager()

        try:
            swagger_manager.create_apidoc()
        except Exception as err:
            print(err.args)

        module = kwargs["module"]
        self.render(module)

    def create_template_loader(self, template_path):
        """Returns a new template loader for the given path.

        May be overridden by subclasses.  By default returns a
        directory-based loader on the given path, using the
        ``autoescape`` and ``template_whitespace`` application
        settings.  If a ``template_loader`` application setting is
        supplied, uses that instead.
        """
        settings = self.application.settings
        if "template_loader" in settings:
            return settings["template_loader"]
        kwargs = {}
        if "autoescape" in settings:
            # autoescape=None means "no escaping", so we have to be sure
            # to only pass this kwarg if the user asked for it.
            kwargs["autoescape"] = settings["autoescape"]
        if "template_whitespace" in settings:
            kwargs["whitespace"] = settings["template_whitespace"]
        return SwaggerYmlLoader(template_path, **kwargs)

