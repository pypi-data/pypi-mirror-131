# @Time    : 2018/3/25 下午1:14
# @Author  : Niyoufa
import re
import os
import sys
import importlib
import traceback
from argparse import ArgumentParser

class CommandError(Exception):
    pass


class BaseCommand(object):
    help = ""

    def handle(self, *args, **options):
        raise NotImplementedError('subclasses of BaseCommand must provide a handle() method')

    def create_parser(self, prog_name, subcommand):
        """
        Create and return the ``ArgumentParser`` which will be used to
        parse the arguments to this command.
        """
        parser = CommandParser(
            self, prog="%s %s" % (os.path.basename(prog_name), subcommand),
            description=self.help or None,
        )
        parser.add_argument(
            '--pythonpath',
            help='A directory to add to the Python path',
        )
        parser.add_argument(
            '--settings',
            help = 'The Python path to a settings module, e.g. myproject.settings'
        )
        self.add_arguments(parser)
        return parser

    def add_arguments(self, parser):
        """
        Entry point for subclassed commands to add custom arguments.
        """
        pass

    def print_help(self, prog_name, subcommand):
        """
        Print the help message for this command, derived from
        ``self.usage()``.
        """
        parser = self.create_parser(prog_name, subcommand)
        parser.print_help()

    def run_from_argv(self, argv):
        """
        Set up any environment changes requested (e.g., Python path
        and settings), then run this command. If the
        command raises a ``CommandError``, intercept it and print it sensibly
        to stderr. If the ``--traceback`` option is present or the raised
        ``Exception`` is not ``CommandError``, raise it.
        """
        self._called_from_command_line = True
        parser = self.create_parser(argv[0], argv[1])
        options = parser.parse_args(argv[2:])
        cmd_options = vars(options)
        args = cmd_options.pop('args', ())
        self.handle_default_options(options)
        self.execute(*args, **cmd_options)

    def execute(self, *args, **options):
        """
        Execute this command
        """
        self.handle(*args, **options)

    def handle_default_options(self, options):
        """
        Include any default options that all commands should accept here
        so that ManagementUtility can handle them before searching for
        user commands.
        """
        if options.pythonpath:
            pythonpaths = [path.strip() for path in re.split(r" ", options.pythonpath) if path.strip()]
            for path in pythonpaths:
                print("pythonpath", path)
                sys.path.insert(0, path)

        if options.settings:
            os.environ.update({"SETTINGS_MODULE":options.settings})
            print("settingspath {settings}".format(settings=options.settings))

    @classmethod
    def get_commands(cls):
        names = [f.split(".py")[0] for f in os.listdir("/".join([os.path.dirname(__file__), "commands"]))
                 if f.endswith(".py")]
        commands = {}
        commands["core"] = {}
        for name in names:
            modulename = "microserver.core.management.commands.{name}".format(
                name=name
            )
            import_module = importlib.import_module(modulename)
            if hasattr(import_module, "Command"):
                command_obj = import_module.Command()
                commands["core"].update({name:command_obj})

        from microserver.conf import settings as const
        COMMANDS = const.COMMANDS or []
        for command_path in COMMANDS:
            abs_command_path = importlib.import_module(command_path).__path__[0]
            names = [f.split(".py")[0] for f in os.listdir("{abs_command_path}/management/commands".format(
                abs_command_path = abs_command_path
            )) if f.endswith(".py")]
            for name in names:
                modulename = "{command_path}.management.commands.{name}".format(
                    command_path = command_path,
                    name=name,
                )

                try:
                    import_module = importlib.import_module(modulename)
                except:
                    print(traceback.format_exc())
                    continue

                if hasattr(import_module, "Command"):
                    command_obj = import_module.Command()
                    commands.setdefault(command_path, {}).update({name:command_obj})
        return commands

    @classmethod
    def get_command_dict(cls):
        command_dict = {}
        commands = cls.get_commands()
        for _, v in commands.items():
            command_dict.update(v)
        return command_dict

class CommandParser(ArgumentParser):
    def __init__(self, cmd, **kwargs):
        self.cmd = cmd
        super(CommandParser, self).__init__(**kwargs)

    def parse_args(self, args=None, namespace=None):
        if (hasattr(self.cmd, 'missing_args_message') and
                not (args or any(not arg.startswith('-') for arg in args))):
            self.error(self.cmd.missing_args_message)
        return super(CommandParser, self).parse_args(args, namespace)

    def error(self, message):
        if self.cmd._called_from_command_line:
            super(CommandParser, self).error(message)
        else:
            raise CommandError("Error: %s" % message)



