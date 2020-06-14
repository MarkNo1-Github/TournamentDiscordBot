from tdbm.logger import GetLogger
from discord.ext.commands import Cog
from discord.ext import commands
from datetime import datetime


__version__ = '0.0.1'


class Initialization(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Log = GetLogger('logs', __name__)

    # Events
    @Cog.listener()
    async def on_ready(self):
        self.Log.debug(f'Bot started {datetime.now()}')
        self.Log.debug(f'Name: {self.bot.user.name}')
        self.Log.debug(f'ID: {self.bot.user.id}')
        guilds = await self.bot.fetch_guilds(limit=150).flatten()
        for guild in guilds:
            self.Log.debug(f"Connected to Guild: {guild} ")

    # Default Vesion Command
    @commands.command()
    async def Initialization_version(self, ctx):
        await ctx.send(f"[Initialization] - version: {__version__}")
        self.Log.debug(f'Bot started {datetime.now()}')

def setup(bot):
    bot.add_cog(Initialization(bot))
