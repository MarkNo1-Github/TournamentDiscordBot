import logging
from logging.handlers import TimedRotatingFileHandler
from logging import Formatter
from pathlib import Path
from datetime import date
import os


__version__ = '0.1.7'

FORMATV2 = '''\
(%(levelname)s) - %(process)d - %(asctime)s\n\t%(name)s::%(filename)s:%(lineno)s\n\t%(funcName)s: %(message)s
'''

FORMAT = '(%(levelname)} s%(asctime)s - pid:%(process)d\n\t%(name)s::%(filename)s:%(lineno)s\n\t%(funcName)s: %(message)s'

# Every 1 Day
ROTATION = 'd'

Success = lambda x : x
Error = lambda y : y


class EnumLogger(object):
    DEBUG = 'debug'
    INFO = 'info'
    WARN = 'warn'
    ERROR = 'error'


class Logger(EnumLogger):
    def __init__(self, name, level=logging.DEBUG):
        self.folder = Path(name)

        # Create Folder if not exist
        if not self.folder.exists():
            self.folder.mkdir()

        # File Log
        self.file_log = Path(name) / f'{name}.{date.today()}.log'

        # Logger
        self.logger = logging.getLogger(name)

        # Handler
        handler = logging.handlers.TimedRotatingFileHandler(self.file_log, when= ROTATION, backupCount=5)
        handler.setFormatter(Formatter(FORMATV2))
        self.logger.addHandler(handler)

        # Set Level
        self.logger.setLevel(level)

        self.callback = {
            self.DEBUG : lambda x : self.logger.debug(x),
            self.INFO : lambda x : self.logger.info(x),
            self.WARN : lambda x : self.logger.warning(x),
            self.ERROR : lambda x : self.logger.error(x),
        }


    def __call__(self, **magic):
        if magic:
            for level, message in magic.items():
                self.callback [level] (message)



if __name__ == '__main__':
    print("** Testing Logger Class **")
    log = Logger('test_logger')
    log(info="START")
    log(debug='debug')
    log(info='info')
    log(warn='warn')
    log(error='error')
    log(info="END", debug="Called after END")
