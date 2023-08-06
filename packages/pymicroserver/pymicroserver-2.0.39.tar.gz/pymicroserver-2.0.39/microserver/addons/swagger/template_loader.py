# @Time    : 2018/5/24 15:57
# @Author  : Niyoufa
from tornado.template import Loader


class SwaggerYmlLoader(Loader):

    def load(self, name, parent_path=None):
        """Loads a template."""
        name = self.resolve_path(name, parent_path=parent_path)
        with self.lock:
            self.templates[name] = self._create_template(name)
            return self.templates[name]