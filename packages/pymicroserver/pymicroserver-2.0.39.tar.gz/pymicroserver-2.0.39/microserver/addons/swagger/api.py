# @Time    : 2018/5/18 16:13
# @Author  : Niyoufa
import os
import re
from microserver.conf import settings
from microserver.core.module import ModuleManager
from microserver.core.handlers import handlers


class SwaggerManager(object):
    """模块管理器"""

    def __init__(self):
        self.swagger_config = self.get_swagger_config()
        self.module_api_docs = {}
        modules = ModuleManager().modules
        swagger_modules = self.swagger_config.get("SWAGGER_MODULES") or []

        for module in modules:
            if not module.module in swagger_modules:
                continue


            module_handlers = sorted(module.handlers, key=lambda obj:obj[0])
            for handler in module_handlers:
                kclass = handler[1]
                if issubclass(kclass, handlers.BaseHandler):
                    doc_content = kclass.__doc__
                    self.module_api_docs.setdefault(module.module, set()).add(doc_content)

    def get_swagger_config(self):
        try:
            swagger_config = settings.SWAGGER
        except:
            swagger_config = {}
        return swagger_config

    def get_module_api_routes(self):
        module_api_routes = []
        for module in self.module_api_docs:
            module_swagger_url =  (self.swagger_config.get("SWAGGER_BASE_URL") or "") + \
                              "%s/%s"%(self.swagger_config.get("SWAGGER_URL"), module.replace(".", "_"))
            module_api_route = ModuleAPIRoute(module, module_swagger_url)
            module_api_routes.append(module_api_route)
        return module_api_routes

    def create_index_file(self):
        description = "模块清单:\n\n" + "\n\n".join([str(obj) for obj in self.get_module_api_routes()])
        title = self.swagger_config.get("SWAGGER_PROJECT_NAME") or ""
        version = host = tags = basePath = schemes = paths = definitions = ""
        api_doc = APIDoc(description, version,
                 title, host, tags, basePath, schemes, paths, definitions)
        content = str(api_doc)

        template_path = settings.get_template_absolute_path()
        swagger_index_filename = self.swagger_config.get("SWAGGER_INDEX_FILENAME") or "index.yml"
        index_path = os.path.join(template_path, swagger_index_filename)
        with open(index_path, "w") as f:
            f.write(content)
        print(swagger_index_filename)
        print(content)

    def create_module_api_file(self):
        template_path = settings.get_template_absolute_path()

        module_api_routes = self.get_module_api_routes()
        for module_api_route in module_api_routes:

            try:
                module_api_path = os.path.join(template_path, module_api_route.module.replace(".", "_") + ".yml")
                description = ""
                title = module_api_route.module
                print("\n********", title + ".yml")
                version = host = basePath = schemes = ""

                tags = "tags:"
                tags += self.parse_module_tags(module_api_route.module)
                print(tags)

                paths = "paths:"
                paths += self.parse_paths(module_api_route.module)
                print(paths)

                definitions = "definitions:"
                definitions += self.parse_definitions(module_api_route.module)
                print(definitions)

                api_doc = APIDoc(description, version,
                     title, host, tags, basePath, schemes, paths, definitions)
                with open(module_api_path, "w") as f:
                    f.write(str(api_doc))
            except Exception as err:
                print(err.args)

    def parse_module_tags(self, module):
        docTags = []
        docs = self.module_api_docs.get(module) or []
        for doc in docs:
            name = ""
            description = ""
            externalDocs = ""
            if not doc:
                continue
            lines = doc.split("\n")
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                match = re.search(r"\@name(.*)", line)
                if match:
                    name += match.group(1).strip()

                match = re.search(r"\@description(.*)", line)
                if match:
                    description += match.group(1).strip()

                match = re.search(r"\@externalDocs(.*)", line)
                if match:
                    externalDocs += match.group(1).strip()
            if name:
                docTag = DocTag(name, description, externalDocs)
                docTags.append(docTag)

        return "\n".join([str(obj) for obj in docTags])

    def parse_paths(self, module):
        path_method_contents = []
        docs = self.module_api_docs.get(module) or []
        for doc in docs:

            if not doc:
                continue

            match = re.search(r"\@path([\s\S]*)\@endpath", doc)
            if match:
                path_content = match.group(1)
                path_method_contents.append(path_content)

        return "\n".join(path_method_contents)

    def parse_definitions(self, module):
        definitions_contents = []
        docs = self.module_api_docs.get(module) or []
        for doc in docs:

            if not doc:
                continue

            match = re.search(r"\@definitions([\s\S]*)\@enddefinitions", doc)
            if match:
                definitions_content = match.group(1)
                definitions_contents.append(definitions_content)

        return "\n".join(definitions_contents)

    def create_apidoc(self):
        template_path = settings.get_template_absolute_path()
        if not os.path.exists(template_path):
            os.makedirs(template_path)
        self.create_index_file()
        self.create_module_api_file()


class ModuleAPIRoute(object):

    def __init__(self, module, module_swagger_url):
        self.module = module
        self.module_swagger_url = module_swagger_url

    def __str__(self):
        return "%s %s"%(self.module, self.module_swagger_url)


class DocTag(object):

    def __init__(self, name, description, externalDocs):
        self.name = name
        self.description = description
        self.externalDocs = externalDocs

    def __str__(self):
        try:
            external_description = self.externalDocs.split(" ")[0]
            external_url = self.externalDocs.split(" ")[1]
        except:
            external_description = ""
            external_url = ""

        content = \
"""
- name: "{name}"
  description: "{description}"
  externalDocs:
    description: "{external_description}"
    url: "{external_url}"
""".format(
    name = self.name,
    description = self.description,
    external_description = external_description,
    external_url = external_url
)
        return content


class APIDoc(object):

    def __init__(self, description, version,
                 title, host, tags, basePath, schemes, paths, definitions):
        self.description = description
        self.version = version
        self.title = title
        self.host = host
        self.tags = tags
        self.basePath = basePath
        self.schemes = schemes
        self.paths = paths
        self.definitions = definitions

    def __str__(self):
        content = \
            """\
swagger: "2.0"
info:
  description: "{description}"
  version: ""
  title: "{title}"
  termsOfService: ""
  contact:
    email: ""
host: ""
basePath: ""
{tags}
{schemes}
{paths}
{definitions}
""".format(
            title=self.title,
            description=self.description,
            tags = self.tags,
            schemes = self.schemes,
            paths = self.paths,
            definitions = self.definitions
        )
        return content



