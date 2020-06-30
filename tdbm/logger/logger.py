import logging
from logging.handlers import TimedRotatingFileHandler
from logging import Formatter
from pathlib import Path
from datetime import date
import os


__version__ = '0.1.7'


FORMAT = f'''%(process)d {'_'}%(levelname)s{'_'} %(asctime)s:%(name)s - %(message)s'''


# Every Day
ROTATION = 'd'

# Discord Labels
Success = lambda x : f"**`SUCCESS`** {x}"
Error = lambda y : f"**`ERROR`** {y}"
Now = lambda : str(date.today())

class Name:
    __name__ = None
    def __init__(self, name):
        self.__name__ = name

class Folder(Name):
    '''
        Folder Class

    '''
    __root_folder__ = None

    def __init__(self, name):
        super().__init__(name)
        self.__root_folder__ = Path( name )
        if not self.__root_folder__.exists():
            self.__root_folder__.mkdir()

class TestFolderName(Folder):
    def __init__(self, name):
        super().__init__(name)
        print(self.__name__)


class Logger(Folder):
    '''
        Logger Class

    '''

    DEBUG = 'debug'
    INFO = 'info'
    WARN = 'warn'
    ERROR = 'error'


    __folder__ = None
    __file__ = None

    def __init__(self, name, level=logging.DEBUG, log_file=True, log_console=True):
        # Call Folder class
        super().__init__(name)

        self.__folder__ = Path(name) / 'logs'

        # Create Folder if not exist
        if not self.__folder__.exists():
            self.__folder__.mkdir()

        # File Log
        self.__file__ = self.__folder__ / Now()

        # Logger
        self.logger = logging.getLogger(name)


        # File Handler
        if log_file:
            file_handler = logging.handlers.TimedRotatingFileHandler(self.__file__, when= ROTATION, backupCount=5)
            file_handler.setFormatter(Formatter(FORMAT))
            self.logger.addHandler(file_handler)

        # Console Handler
        if log_console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(Formatter(FORMAT))
            self.logger.addHandler(console_handler)

        # Set Level default DEBUG
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
    log_folder = 'test_logger'
    log = Logger(log_folder)
    log(info="** Testing Logger Class **")
    log(info="START")
    log(debug='This is an example of a level of log case of the type: debug')
    log(info='This is an example of a level of log case of the type: info')
    log(warn='This is an example of a level of log case of the type: warn')
    log(error='This is an example of a level of log case of the type: error')
    log(**{'info': 'osdjfosjfosjfd'})
    log(info="END", debug="Called after END")
