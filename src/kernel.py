from src.lib import parser
from src.lib import executor
from src.lib import downloader
from etc import loader

from os import system as cmd
from platform import platform as _os

class Kernel:
    def __init__(self, shell):
        self.shell = shell

    def exec(self, command):
        command, args = parser.listit(command)
        return executor.exec(command, args)

    def startup(self):
        config = loader.yml('config.yml')

        # configuration
        if _os == 'Windows':
            cmd(f'title {config["shell"]["name"]}')

        if config["startup"]["message"] != None:
            self.shell.send(config["startup"]["message"])      

        if config["startup"]["commands"] != [None]:
            for el in config["startup"]["commands"]:
                self.shell.send(exec(el))

    def loop(self):
        while True:
            command = self.shell.read()
            command, args = parser.listit(command)

            if command == 'g':
                downloader.download_command(args[0])

            self.shell.send(exec(command))
