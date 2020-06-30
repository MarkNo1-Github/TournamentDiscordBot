import logging
from logging.handlers import TimedRotatingFileHandler
from logging import Formatter
from pathlib import Path
from datetime import date
import os


__version__ = '0.1.7'


FORMAT = f'''\
 %(process)d {'_'}%(levelname)s{'_'} %(asctime)s:%(filename)s:%(lineno)s:%(name)s:%(funcName)s
    %(message)s'''


# Every Day
ROTATION = 'd'

# Discord Labels
Success = lambda x : f"**`SUCCESS`** {x}"
Error = lambda y : f"**`ERROR`** {y}"


class EnumLogger(object):
    DEBUG = 'debug'
    INFO = 'info'
    WARN = 'warn'
    ERROR = 'error'


class Logger(EnumLogger):
    def __init__(self, name, level=logging.DEBUG, log_file=True, log_console=True):
        self.folder = Path(name) / 'logs'

        # Create Folder if not exist
        if not self.folder.exists():
            self.folder.mkdir()

        # File Log
        self.file_log = Path(name) / f'{name}.{date.today()}'

        # Logger
        self.logger = logging.getLogger(name)


        # File Handler
        if log_file:
            file_handler = logging.handlers.TimedRotatingFileHandler(self.file_log, when= ROTATION, backupCount=5)
            file_handler.setFormatter(Formatter(FORMAT))
            self.logger.addHandler(file_handler)

        # Console Handler
        if log_console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(Formatter(FORMAT))
            self.logger.addHandler(console_handler)

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
    log_file = 'test_logger'
    log = Logger('test_logger')
    log(info="** Testing Logger Class **")
    log(info="START")
    log(debug='debug')
    log(info='info')
    log(warn='warn')
    log(error='error')
    log(info="END", debug="Called after END")
