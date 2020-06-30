from pathlib import Path
from tdbm.logger import Logger, Success, Error, Now
import os
import pandas as pd
from pandas import read_hdf
from datetime import date
from tabulate import tabulate



class IData:
    def __init__(self, **kw):
        self.__dict__ = kw
        self.__dict__.update({'created':date.today()})

    def __str__(self):
        return str(self.__dict__)


class HDFLogger(Logger):
    __init_times = 0
    __read_times = 0
    __write_times = 0
    __wrror_times = 0

    __INIT__  = lambda self : super().__call__(debug=f'Initialization File: {self.__file__}')
    __READ_OK__ = lambda self : super().__call__(debug=f'Read File: {self.__file__}')
    __WRITE_OK__ = lambda self : super().__call__(debug=f'Write File: {self.__file__}')
    __READ_ERROR__  = lambda self, error: super().__call__(error=f'Read File: {self.__file__} - Error: {error}')
    __WRITE_ERROR__ = lambda self, error : super().__call__(error=f'Write File: {self.__file__} - Error: {error}')


class HDFData(HDFLogger):
    '''
        Logger Class

    '''

    __folder__ = None
    __file__ = None

    def __init__(self, name, DataType):
        # Call Folder class
        super().__init__(name)

        self.__folder__ = Path(name) / 'data'
        self.__file__ = self.__folder__ / self.__name__ 

        # Create Folder if not exist
        if not self.__folder__.exists():
            self.__folder__.mkdir()

        self.DataType = DataType


    def __call__(self, data=None):
        if isinstance(data, pd.DataFrame):
            self.__write__(data)
        else:
            return self.__read__()


    def __read__(self):
        try:
            if self.__file__.exists():
                super().__READ_OK__()
                return read_hdf(self.__file__, self.__name__, 'r')
            else:
                super().__INIT__()
                return pd.DataFrame(columns=list(self.DataType().__dict__.keys()))

        except Exception as e:
            super().__READ_ERROR__(e)
            return None


    def __write__(self, data):
        try:
            mode = 'a' if self.__file__.exists() else 'w'
            data.to_hdf(self.__file__, self.__name__, mode)
            super().__WRITE_OK__()

        except Exception as e:
            super().__WRITE_ERROR__(e)




if __name__ == '__main__':
    data_folder = 'test_data'
    data = HDFData(data_folder, IData)
    test = data()
    data(test)
