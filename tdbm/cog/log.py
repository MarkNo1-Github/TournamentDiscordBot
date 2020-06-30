# from tdbm.logger import GetFileLogger, Success, Error
from tdbm.data import DataManager
from tdbm.logger import Logger
from discord.ext.commands import Cog
from discord.ext import commands
from datetime import datetime


__version__ = '0.0.1'


class LoggerExtension(Cog):
    '''
     <EXTENSION LOG>

    '''
    def __init__(self, bot):
        self.bot = bot
        self.Log = Logger(__name__)

    async def log_all(self, message):
        '''
            LOG in all Channels of all Guilds
        '''
        self.Log(debug=message)
        for guild in self.bot.guilds:
            for channel in guild.text_channel:
                await channel.send(message)

    @Cog.listener()
    async def on_ready(self):
        self.Log(debug=f'{__name__}: Extension ready on {self.bot.user}:{self.bot.user.id}')
        await self.log_all(f'{__name__}: Extension ready on {self.bot.user}')


def setup(bot):
    bot.add_cog(LoggerExtension(bot))
