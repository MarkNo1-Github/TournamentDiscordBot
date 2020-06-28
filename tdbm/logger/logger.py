import logging
from logging.handlers import TimedRotatingFileHandler
from logging import Formatter
from pathlib import Path
from datetime import date
import os


__version__ = '0.1.7'

FORMATV2 = '''\
(%(levelname)s) %(asctime)s - pid:%(process)d\n\t%(name)s::%(filename)s:%(lineno)s\n\t%(funcName)s: %(message)s
'''
FORMAT = '(%(levelname)} s%(asctime)s - pid:%(process)d\n\t%(name)s::%(filename)s:%(lineno)s\n\t%(funcName)s: %(message)s'

# Every 1 Day
ROTATION = 'd'

Success = lambda x : x
Error = lambda y : y


class EnumLogger(object):
    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3


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


    def __call__(self, level: EnumLogger, *args, **kargs):
        if args:
            self.callback [level] (*args)
        if kargs:
            self.callback [level] (kargs)







def GetFileLogger(folder, name):
    import logging
    from logging.handlers import TimedRotatingFileHandler
    logger = logging.getLogger(name)

    if not os.path.exists(folder):
        os.makedirs(folder)

    hdlr = TimedRotatingFileHandler(os.path.join(folder, f'{name}.{date.today()}.log'),  when='d', backupCount=5)
    formatter = logging.Formatter('%(asctime)s::%(process)d::%(levelname)s::%(name)s::%(filename)s:%(lineno)s::%(funcName)s: %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger


if __name__ == '__main__':
    print("** Testing Logger Class **")
    log = Logger('test_logger')
    log(log.DEBUG, 'debug')
    log(log.INFO, 'info')
    log(log.WARN, 'warn')
    log(log.ERROR, 'error')
