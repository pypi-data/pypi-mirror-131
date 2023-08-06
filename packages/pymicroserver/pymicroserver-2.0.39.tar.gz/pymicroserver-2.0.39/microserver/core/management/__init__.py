# @Time    : 2018/3/12 15:31
# @Author  : Niyoufa
import re
import os
import sys
import microserver
from microserver.core.management.base import BaseCommand
from microserver.core.management.base import CommandError
from microserver.core.management.base import CommandParser


class ManagementUtility(object):

    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])

    def execute(self):
        try:
            subcommand = self.argv[1]
        except IndexError:
            subcommand = "help"

        parser = CommandParser(None, usage="%(prog)s subcommand [options] [args]", add_help=False)
        parser.add_argument('--pythonpath')
        parser.add_argument('--settings')
        parser.add_argument('args', nargs='*')

        options, args = parser.parse_known_args(self.argv[2:])
        self.handle_default_options(options)

        if subcommand == 'help' or self.argv[1:] in (['--help'], ['-h']):
            commands = BaseCommand.get_commands()
            for k, v in commands.items():
                print(k)
                for command_name, command_obj in v.items():
                    command_info = command_obj.__doc__
                    if command_info:
                        command_info = command_info.strip()
                    else:
                        command_info = ""
                    print("{command_name} {command_info}".format(
                        command_name = command_name,
                        command_info = command_info
                    ))
                print()
        elif self.argv[2:] in (['--help'], ['-h']):
            kclass = self.fetch_command(subcommand)
            kclass.print_help(self.prog_name, subcommand)
        elif subcommand == 'version' or self.argv[1:] == ['--version']:
            print("{version}".format(version=microserver.__version__) + '\n')
        elif subcommand == 'shell':
            self._ipython()
        else:
            kclass = self.fetch_command(subcommand)
            if kclass:
                kclass.run_from_argv(self.argv)

    def _ipython(self):
        """Start IPython >= 1.0"""
        from IPython import start_ipython
        start_ipython(argv=[])

    def fetch_command(self, subcommand):
        command_dict = BaseCommand.get_command_dict()
        if subcommand in command_dict:
            command_obj = command_dict[subcommand]
            if not isinstance(command_obj, BaseCommand):
                raise CommandError("命令类型错误：{}")
            return command_obj
        else:
            raise CommandError("'{command}'命令不存在".format(command=subcommand))

    def handle_default_options(self, options):
        """
        Include any default options that all commands should accept here
        so that ManagementUtility can handle them before searching for
        user commands.
        """
        if options.pythonpath:
            pythonpaths = [path.strip() for path in re.split(r",", options.pythonpath) if path.strip()]
            for path in pythonpaths:
                print("pythonpath", path)
                sys.path.insert(0, path)

        if options.settings:
            os.environ.update({"SETTINGS_MODULE": options.settings})
            print("settingspath {settings}".format(settings=options.settings))

def execute_from_command_line(argv=None):
    """
    A simple method that runs a ManagementUtility.
    """
    utility = ManagementUtility(argv)
    utility.execute()