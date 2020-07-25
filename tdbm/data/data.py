from pathlib import Path
from tdbm.logger import Logger, Success, Error, Now
import os
import pandas as pd
from pandas import read_hdf
from datetime import datetime
from tabulate import tabulate



class IData:
    def __init__(self, **kw):
        self.__dict__ = kw
        self.__dict__.update({'id':int()})
        self.__dict__.update({'created':pd.Timestamp(datetime.now())})

    def __str__(self):
        return str(self.__dict__)

    def __call__(self):
        return self.__dict__

    def as_series(self):
        return pd.Series(self.__dict__)


class HDFControllerLogger(Logger):
    _init_times = 0
    _read_times = 0
    _write_times = 0
    _error_times = 0

    # HDFController
    __class_name__ = "HDFControllerLogger"
    __INIT__  = lambda self : super().__call__(debug=f'[{self.__class_name__}]: Start on file: {self.__file__}')
    __DATA_INIT__ = lambda self : super().__call__(debug=f'[{self.__class_name__}]: Initialization File: {self.__file__}')
    __READ_OK__ = lambda self : super().__call__(debug=f'[{self.__class_name__}]: Read file')
    __WRITE_OK__ = lambda self : super().__call__(debug=f'[{self.__class_name__}]: Write file')
    __READ_ERROR__  = lambda self, error: super().__call__(error=f'[{self.__class_name__}]: Read File: {self.__file__} - Error: {error}')
    __WRITE_ERROR__ = lambda self, error : super().__call__(error=f'[{self.__class_name__}]: Write File: {self.__file__} - Error: {error}')
    __COUNTERS__ = lambda self, : f"Counters: init:{self._init_times} - read:{self._read_times} - write:{self._write_times} - error:{self._error_times}"
    __CHECKPOINT__ = lambda self: super().__call__(debug=f'[{self.__class_name__}]: Destruction. {self.__COUNTERS__()}')




class HDFController(HDFControllerLogger):
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
        self.__INIT__()


    def __call__(self, data=None):
        if isinstance(data, pd.DataFrame):
            return self.__write__(data)
        else:
            return self.__read__()


    def __read__(self):
        try:
            if self.__file__.exists():
                super().__READ_OK__()
                self._read_times += 1
                return read_hdf(self.__file__, self.__name__, 'r')
            else:
                super().__DATA_INIT__()
                self._init_times += 1
                return self.__create_dataframe__()

        except Exception as e:
            super().__READ_ERROR__(e)
            self._error_times += 1
            return None


    def __write__(self, data):
        try:
            mode = 'a' if self.__file__.exists() else 'w'
            data.to_hdf(self.__file__, self.__name__, mode, format='table')
            super().__WRITE_OK__()
            self._write_times += 1
            return True

        except Exception as e:
            super().__WRITE_ERROR__(e)
            self._error_times += 1
            return False

    def __create_dataframe__(self):
        data = pd.DataFrame(self.DataType(), index=[1])
        data = data[0:0]
        return data

    def __status__(self):
        super().__CHECKPOINT__()

    def __del__(self):
        self.__status__()

    def __show__(self, data):
        return "```" + f'\n{tabulate(data, headers="keys", tablefmt="plain")}' + "\n```"



class HDFDataLogger:

    __class_name__ = "HDFDataLogger"
    __INIT__  = lambda self : self.__log__(debug=f'[{self.__class_name__}]: Start')
    __SAVE_OK__  = lambda self : self.__log__(debug=f'[{self.__class_name__}]: Save data ')
    __SAVE_ERROR__  = lambda self : self.__log__(error=f'[{self.__class_name__}]: Save data - ERROR')
    __LOAD__  = lambda self : self.__log__(debug=f'[{self.__class_name__}]: Load data')
    __RESET__ = lambda self : self.__log__(debug=f'[{self.__class_name__}]: Reset data')
    __NEW_ROW__ = lambda self, id : self.__log__(debug=f'[{self.__class_name__}]: New row with ID:{id}')
    __REMOVE_OK__ = lambda self, col, val : self.__log__(debug=f'[{self.__class_name__}]: Removed record with col:{col} and val:{val}')
    __REMOVE_ERROR__ = lambda self, col, val : self.__log__(error=f'[{self.__class_name__}]: Removed Error - No record found with col:{col} and val:{val}')
    __MODIFY_OK__ = lambda self, col, val, new_val : self.__log__(debug=f'[{self.__class_name__}]: Modified record with col:{col} val:{val}->{new_val}')
    __MODIFY_ERROR__ = lambda self, col, val, new_val : self.__log__(error=f'[{self.__class_name__}]: Modified Error - No record found with col:{col} val:{val}->{new_val}')


    def __init__(self, name, DataType):
        self.controller = HDFController(name, DataType)
        self.__log__ = self.controller.__log__
        self.data = self.controller()
        self.counter_id = 0
        self.DataType = DataType
        if isinstance(self.DataType, IData):
            self.counter_id = self.DataType()['id']
        elif not self.data.empty:
                self.counter_id = self.data['id'].max()
        self.__INIT__()



class HDFData(HDFDataLogger):

    def save(self):
        if self.controller(self.data):
            self.__SAVE_OK__()
        else:
            self.__SAVE_ERROR__()

    def load(self):
        self.data = self.controller()
        self.__LOAD__()
        return True

    def reset(self):
        self.controller(self.controller.__create_dataframe__())
        self.data = self.controller()
        self.counter_id = 0
        self.__RESET__()
        return True

    def add(self, rowclass: IData):
        rowclass.id = self.get_id()
        self.data = self.data.append(rowclass.as_series(), ignore_index=True)
        self.__NEW_ROW__(self.counter_id)
        return True

    def remove(self, col, value):
        to_remove = self.data.loc[self.data[col] == value]
        if not to_remove.empty:
            self.data = self.data[self.data[col] != value]
            self.__REMOVE_OK__(col, value)
            return True
        else:
            self.__REMOVE_ERROR__(col, value)
            return False

    def modify(self, col, value, new_val):
        to_modify = self.data.loc[self.data[col] == value]
        if not to_modify.empty:
            self.data.loc[self.data[col] == value, col] = new_val
            self.__MODIFY_OK__(col, value, new_val)
            return True
        else:
            self.__MODIFY_ERROR__(col, value, new_val)
            return False

    def get_id(self):
        self.counter_id += 1
        return self.counter_id

    def show(self):
        return self.controller.__show__(self.data)



if __name__ == '__main__':
    data_folder = 'test_data'

    MyDataTypes = IData(name="", surname="", email="", address="", age=int(), heigh=float())

    data = HDFData(data_folder, MyDataTypes)
    data.add(IData(name="Marco", surname="Treglia", email="cool@yeah.it", address="secret", age=28, heigh=1.75))
    print(data.show())
    data.save()
    data.modify("name", "Marco", "Mark")
    print(data.show())
    data.remove("id", 0)
    print(data.show())
    data.save()
    data.reset()
    print(data.show())
    data.save()
