# @Time    : 2018/3/25 下午9:35
# @Author  : Niyoufa
import os
import shutil
from importlib import import_module
from microserver.core import template
from microserver.core.management.base import BaseCommand
from microserver.core.management.base import CommandError
from microserver.utils.print import green_print
from microserver.utils import dir


class Command(BaseCommand):
    """
    创建模块
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "modulename",
            help=("模块名称"),
            type=lambda x: self.check_modulename(x)
        )

    def check_modulename(self, modulename):
        if not modulename:
            raise CommandError("you must provide a modulename")
        elif not modulename.isidentifier():
            raise CommandError("'{modulename}' is not a valid module identifier".format(
                modulename = modulename
            ))
        else:
            try:
                import_module(modulename)
            except:
                pass
            else:
                raise CommandError("'{modulename}' conflicts with the name of an existing Python Module".format(
                    modulename = modulename
                ))

        return modulename

    def get_default_modulepath(self):
        return os.path.abspath(".")

    def handle(self, *args, **options):
        self.modulename = options["modulename"]
        self.modulepath = os.path.join(self.get_default_modulepath(), self.modulename)

        def file_handle(root, file):
            if file.endswith("-tpl"):
                old_file = os.path.join(root, file)
                new_file = os.path.join(self.modulepath, file[:-4])
                shutil.copyfile(old_file, new_file)
                with open(new_file, "r") as f:
                    file_content = f.read()
                    file_content = file_content.replace("{ModuleName}", self.modulename.split("_")[0].capitalize())\
                    .replace("{module_name}", self.modulename.split("_")[0])

                with open(new_file, "w") as f:
                    f.write(file_content)

        try:
            os.makedirs(self.modulepath)
            dir.traverse_tree(template.get_module_template_path(), file_handle=file_handle)
        except FileExistsError:
            raise CommandError("module has exists")

        green_print("module {modulename} create success: {modulepath}".format(
            modulename = self.modulename,
            modulepath = self.modulepath
        ))