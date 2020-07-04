from tdbm.logger import Logger, Success, Error, Normal
from discord.ext.commands import Cog
from discord.ext import commands


__version__ = '0.0.4'


class LoggerExtension(Cog):
    '''
     <EXTENSION LOG>

    '''
    def __init__(self, name, bot):
        self.bot = bot
        self.name = name
        self.Log = Logger(name)

    @Cog.listener()
    async def on_ready(self):
        '''
            Send message when the extension is ready
        '''
        await self.send_all_channels(f'Online on {self.bot.user}')


    def extension_message(self, message):
        '''
            Add extension name to message
        '''
        return f'Extension ({self.name}) - {message}'


    async def send_message(self, message, ctx, status=Normal):
        '''
            Send message to the log and to the channel set in ctx
        '''
        message = self.extension_message(message)
        if status == Error:
            self.Log(error=message)
        else:
            self.Log(debug=message)
        await ctx.send(status(message))

    def log_message(self, level, message):
        self.Log(**{level:message})



    async def send_all_channels(self, message):
        '''
            Send message in all Channels of all Guilds
        '''
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                await self.send_message(message, channel, Success)
