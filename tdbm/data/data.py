from tdbm.logger import GetFileLogger, Success, Error
import os
import pandas as pd
from pandas import read_hdf
from datetime import date

class FileRaidEnum:
    init = lambda name :  f'Initialization File: {name}'
    reading = 'Reading'
    writing = 'Writing'
    exit = lambda self, type, val, tb :  f'Exiting File: {type} {val} {tb}'
    file_path = lambda self, name, path : f'Path file {name}: {path}'


class DataController(object):
    def __init__(self, name):
        self.__doc__ = '''

        '''
        self.name = name
        self.dp = os.path.dirname(os.path.abspath(os.getcwd()))
        self.dp = os.path.join(self.dp, name)
        self.fp = os.path.join(self.dp, f'{name}.data')
        self.logger = GetFileLogger(self.dp, f'{name}.store')
        self.enum = FileRaidEnum()
        self.logger.debug(self.enum.file_path('Directory', self.dp))
        self.logger.debug(self.enum.file_path('Data File', self.fp))
        self.logger.debug(self.enum.file_path('Log File', f'{self.dp}/{name}.store'))

    def __enter__(self):
        self.logger.debug(Success(self.enum.reading))

    def __exit__(self, type, val, tb):
        self.logger.debug(self.exit(type,val,tb))

    def __call__(self, data=None):
        if isinstance(data, pd.DataFrame):
            self.write(data)
        else:
            return self.read()

    def read(self):
        try:
            data = read_hdf(self.fp, key=self.name, mode='r')
            self.logger.debug(Success(self.enum.reading))
            return data
        except Exception as e:
            self.logger.debug(Error(f'{e}'))
            return pd.DataFrame()

    def write(self, data):
        try:
            if self.already_exist():
                mode = 'a'
            else:
                mode = 'w'
            data.to_hdf(self.fp, key=self.name, mode=mode)
            self.logger.debug(Success(self.enum.writing))
        except Exception as e:
            self.logger.debug(Error(f'{e}'))

    def already_exist(self):
        return os.path.exists(self.fp)

    def __str__(self):
        return self.fp



class IData:
    def __init__(self, name='Init', id=0):
        self.created = date.today()
        self.id = id
        self.name = name



class DataManager(object):
    def __init__(self, name, dataType: IData):
        self.controller = DataController(name)
        self.data = self.controller()

        self.counter_id = 0
        if self.data.empty:
            temp = dataType()
            self.data = pd.DataFrame(columns=list(temp.__dict__.keys()))
            self.add(temp)
        else:
            self.counter_id = self.data['id'].max()
        self.controller.logger.debug(Success('Initialization'))

    def add(self, rowclass: IData):
        rowclass.id = self.get_counter()
        self.data = self.data.append(pd.Series(rowclass.__dict__), ignore_index=True)
        self.controller.logger.debug(Success('Row added'))

    def remove(self, col_val, value):
        self.data = self.data[self.data[col_val] != value]
        self.controller.logger.debug(Success('Row removed'))

    def __exit__(self, type, val, tb):
        self.save()
        self.controller.logger.debug(self.exit(type,val,tb))

    def save(self):
        self.controller(self.data)
        self.controller.logger.debug(Success('Save'))

    def load(self):
        self.data = self.controller()
        self.controller.logger.debug(Success('Load'))

    def get_counter(self):
        self.counter_id += 1
        return self.counter_id
