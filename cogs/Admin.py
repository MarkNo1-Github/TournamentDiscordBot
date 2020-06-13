from discord.ext.commands import Cog
from discord.ext import commands

__version__ = '0.0.1'

class Admin(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def load_extension(self, ctx, extension):
        self.bot.load_extension(f'cogs.{extension}')
        await ctx.send(f"Extension: {extension} Loaded!")


    @commands.command()
    async def unload_extension(self, ctx, extension):
        self.bot.unload_extension(f'cogs.{extension}')
        await ctx.send(f"Extension: {extension} Unloaded!")


    @commands.command()
    async def reload_extension(self, ctx, extension):
        self.bot.unload_extension(f'cogs.{extension}')
        self.bot.load_extension(f'cogs.{extension}')
        await ctx.send(f"Extension: {extension} Reloaded!")

    # Default Vesion Command
    @commands.command()
    async def Admin_version(self, ctx):
        await ctx.send(f"[Admin] - version: {__version__}")

def setup(bot):
    bot.add_cog(Admin(bot))
