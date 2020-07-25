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
    def __init__(self, name, bot):
        super().__init__(name, bot)
        self.Datas = dict()

    def register_database(self, db_name, DataType):
        self.Datas.update({db_name : HDFData(f"HDF{db_name}", DataType)})
        self.log_message({'debug':f"Database {db_name} initialized"})

    def dictionary_from_arg(self, arg):
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
            pre_data.update(self.dictionary_from_arg(arg))
        return IData(**pre_data)


    @commands.command()
    async def create_database(self, ctx, db_name, DataType=None, *args):
        """ Create a database by args or by DataType """
        if not DataType:
            try:
                DataType = self.__IData_from_args__(args)
            except Exception as e:
                await self.send_message(f"Error parsing arguments: {e}", ctx, Error)
        else:
            self.Datas.update({db_name : HDFData(f"HDF{db_name}", DataType)})


    @commands.command()
    async def add_row(self, ctx, db_name, *args):
        """Add row to pandas dataframe"""
        try:
            print(db_name)
            print(args)
            self.Datas[db_name].add(self.__IData_from_args__(args))
            await self.send_message(f"Row added from {db_name}", ctx, Success)
        except Exception as e:
            await self.send_message(f"Error parsing arguments for {db_name}: {e}", ctx, Error)


    @commands.command()
    @commands.is_owner()
    async def remove_row(self, ctx, db_name, col, val):
        """Remove row to pandas dataframe"""
        if self.Datas[db_name].remove(col, val):
            self.send_message(f"Row removed from {db_name}", ctx, Success)
        else:
            self.send_message(f"Error - removing Row from {db_name}", ctx, Error)


    @commands.command()
    async def modify_row(self, ctx, db_name, col, val, new_val):
        """Modify row to pandas dataframe"""
        if self.Datas[db_name].modify(col, val, new_val):
            self.send_message(f"Row modified from {db_name}", ctx, Success)
        else:
            self.send_message(f"Error - modifing Row from {db_name}", ctx, Error)


    @commands.command()
    async def show_data(self, ctx, db_name):
        """ Show Data """
        self.log_message({'debug':'requested show_data'})
        await ctx.send(f"Database: {db_name}" + self.Datas[db_name].show())


    @commands.command()
    async def show_datas(self, ctx):
        """ Show Data """
        self.log_message({'debug':'requested show_data'})
        for db_name in self.Datas.keys():
            await self.show_data(ctx, db_name)


    @commands.command()
    async def show_preformat_data_record(self, ctx, db_name, excluded=[]):
        """ Show preformat data """
        await ctx.send(f'Database: {db_name} | ' + ' '.join([f'{x}=' for x in self.Datas[db_name].DataType() if x not in ['id', 'created'] + excluded]))


    @commands.command()
    async def show_all_preformat_data_record(self, ctx):
        """ Show all preformat data """
        for db_name in self.Datas.keys():
            await self.show_preformat_data_record(ctx, db_name)
