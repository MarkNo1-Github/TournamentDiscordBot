from logging.handlers import TimedRotatingFileHandler
from datetime import date
import logging
import os

def GetLogger(folder, name):
    logger = logging.getLogger(name)

    if not os.path.exists(folder):
        os.makedirs(folder)

    hdlr = TimedRotatingFileHandler(os.path.join(folder, f'{name}.{date.today()}.log'),  when='d', backupCount=5)
    formatter = logging.Formatter('%(asctime)s::%(process)d::%(levelname)s::%(name)s::%(filename)s:%(lineno)s::%(funcName)s: %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger

def Success(txt):
    return "**`SUCCESS`** " + str(txt)

def Error(txt):
    return "**`ERROR`** " + str(txt)
