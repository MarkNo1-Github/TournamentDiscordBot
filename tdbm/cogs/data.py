# from tdbm.logger import GetFileLogger, Success, Error
from tdbm.data import HDFData, IData
from tdbm.logger import Success, Error, Normal
from tdbm.cogs import LoggerExtension
from discord.ext.commands import Cog
from discord.ext import commands
from datetime import datetime


__version__ = '0.0.1'


class DataExtension(LoggerExtension):
    '''
     <EXTENSION LOG>

    '''
    def __init__(self, name, bot, DataType):
        super().__init__(name, bot)
        self.DataType = DataType
        self.Data = HDFData(f"HDF{name}", DataType)

    def __dictionary_from_arg__(self, arg):
        '''
            Parse 1 arg into dictionary
        '''
        if '=' in arg:
            key = arg.split('=')[0]
            val = arg.split('=')[1]
            if not key in self.DataType().keys():
                raise Exception(f"Wrong key -> {key}")
            return {key:val}

    def __IData_from_args__(self, args):
        '''
            Parse all args into IData
        '''
        pre_data = {}
        for arg in args:
            pre_data.update(self.__dictionary_from_arg__(arg))
        return IData(**pre_data)


    @commands.command()
    async def add_row(self, ctx, *args):
        """Add row to pandas dataframe"""
        try:
            self.Data.add(self.__IData_from_args__(args))
            await self.send_message("Row added", ctx, Success)
        except Exception as e:
            await self.send_message(f"Error parsing arguments: {e}", ctx, Error)

    @commands.command()
    async def show_data(self, ctx):
        self.log_message('debug', 'requested show_data')
        await ctx.send(self.Data.show())


    @commands.command()
    async def example_data_record(self, ctx):
        await ctx.send(' '.join([f'{x}=' for x in self.DataType()]))
