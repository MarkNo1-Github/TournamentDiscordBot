from pathlib import Path
from tdbm.logger import GetFileLogger, Success, Error
import os
import pandas as pd
from pandas import read_hdf
from datetime import date
from tabulate import tabulate



def show_data(data):
    return "```" + f'\n\n{tabulate(data, headers="keys", tablefmt="plain")}' + "```"


def dataFromDiscordArgs(args):
    pre_data = {}
    try:
        for arg in args:
            if '=' in arg:
                key = arg.split('=')[0]
                val = arg.split('=')[1]
                pre_data.update({key:val})
    except Exception as e:
        print("Error:", e)
        return None
    return IData(**pre_data)


class EnumFile:
    init = lambda name :  f'Initialization File: {name}'
    reading = 'Reading'
    data_not_created = 'Data file is not created yet.'
    writing = 'Writing'
    exit = lambda self, type, val, tb :  f'Exiting File: {type} {val} {tb}'
    file_path = lambda self, name, path : f'Path file {name}: {path}'




class EnumLoggerMessage:
    log_init = lambda name :  f'Initialization File: {name}'
    log_reading = 'Reading'
    log_data_to_init = 'Data file is not created yet. Performing Initialization'
    log_writing = 'Writing'
    log_exit = lambda self, type, val, tb :  f'Exiting File: {type} {val} {tb}'
    log_file_path = lambda self, name, path : f'Path file {name}: {path}'



class DataControllerLogger(EnumLoggerMessage):
    def __init__(self, Name):
        '''
            Class to Manage Folder's Structure
        '''
        self.name = Name
        self.logger =  GetFileLogger(self.current_path, f'{name}.log')
        self.data_path = os.path.join(self.current_path, Name)
        self.fp = os.path.join(self.dp, f'{name}.data')




class DataController(object):
    def __init__(self, Name, DataBaseClass):
        self.__doc__ = '''

        '''
        self.name = Name
        self.dp = os.path.dirname(os.path.abspath(os.getcwd()))
        self.dp = os.path.join(self.dp, name)
        self.fp = os.path.join(self.dp, f'{name}.data')
        self.logger = GetFileLogger(self.dp, f'{name}.store')
        self.enum = FileRaidEnum()
        self.logger.debug(self.enum.file_path('Directory', self.dp))
        self.logger.debug(self.enum.file_path('Data File', self.fp))
        self.logger.debug(self.enum.file_path('Log File', os.path.join(self.dp, f'{name}.store')))
        self.DataBaseClass = DataBaseClass

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
            if self.already_exist():
                data = read_hdf(self.fp, key=self.name, mode='r')
                self.logger.debug(Success(self.enum.reading))
                return data
            else:
                self.logger.info(Success(self.enum.response_data_to_init))
                return self.create_database()
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

    def create_database(self):
        temp = self.DataBaseClass()
        return pd.DataFrame(columns=list(temp.__dict__.keys()))

    def already_exist(self):
        return os.path.exists(self.fp)

    def __str__(self):
        return self.fp



class IData:
    def __init__(self, **kw):
        self.__dict__ = kw
        self.__dict__.update({'created':date.today()})

    def __str__(self):
        return str(self.__dict__)


class DataManager(object):
    def __init__(self, name):
        self.controller = DataController(name, IData)
        self.data = self.controller()

        self.counter_id = 0
        if not self.data.empty:
            self.counter_id = self.data['id'].max()

        self.controller.logger.debug(Success('Initialization'))

    def add_from_args(self, args):
        try:
            record = dataFromDiscordArgs(args)
            record.id = self.get_counter()
            self.data = self.data.append(pd.Series(record.__dict__), ignore_index=True)
            self.controller.logger.debug(Success('Row added'))
        except Exception as e:
            self.controller.logger.debug(Error(f'Error adding row {e}'))

    def add(self, rowclass: IData):
        rowclass.id = self.get_counter()
        self.data = self.data.append(pd.Series(rowclass.__dict__), ignore_index=True)
        self.controller.logger.debug(Success('Row added'))

    def remove(self, col, value):
        to_remove = self.data.loc[self.data[col] == value]
        if not to_remove.empty:
            self.data = self.data[self.data[col] != value]
            self.controller.logger.debug(Success('Row removed'))
            return Success("Correct removed: \n" + show_data(to_remove))
        else:
            self.controller.logger.debug(Error('No row to removed'))
            return Error("No record found with col:{col} and val:{value}")

    def __exit__(self, type, val, tb):
        self.save()
        self.controller.logger.debug(self.exit(type,val,tb))

    def modify(self, col, value, new_val):
        to_modify = self.data.loc[self.data[col] == value]
        if not to_modify.empty:
            to_modify[col] = new_val
            self.data.loc[self.data[col] == value] = to_modify
            return Success("Correct modify to: \n" + show_data(to_modify))
        else:
            self.controller.logger.debug(Error('No row to modify'))
            return Error("No record found with col:{col} and val:{value}")

    def modify_byid(self, id, col, new_val):
        id = int(id)
        to_modify = self.data.loc[self.data['id'] == id]
        if not to_modify.empty:
            to_modify[col] = new_val
            self.data.loc[self.data['id'] == id] = to_modify
            return Success("Correct modified: \n" + show_data(to_modify))
        else:
            self.controller.logger.debug(Error('No row to modify'))
            return Error("No record found with col:{col} and val:{value}")


    def save(self):
        self.controller(self.data)
        self.controller.logger.debug(Success('Save'))

    def load(self):
        self.data = self.controller()
        self.controller.logger.debug(Success('Load'))

    def reset(self):
        self.controller(self.controller.create_database())
        self.data = self.controller()
        self.controller.logger.debug(Success('Reset'))

    def show(self):
        return Success(show_data(self.data))

    def get_counter(self):
        self.counter_id += 1
        return self.counter_id
