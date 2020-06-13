import os
import argparse
from string import Template


__version__ = '0.0.1'


code = Template('''from tdb.logger import GetLogger
from discord.ext.commands import Cog
from discord.ext import commands
from datetime import datetime

__version__ = '0.0.1'

class $Extension(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Log = GetLogger('logs', __name__)

    # Events
    #@Cog.listener()

    # Default Vesion Command
    @commands.command()
    async def ${Extension}_version(self, ctx):
        await ctx.send(f"[$Extension] - version: {__version__}")
        self.Log.debug(f'Call on version')

def setup(bot):
    bot.add_cog($Extension(bot))
''')


# Command to create new Extension
def new_extension(Extension: str):
    extension_path = os.path.join('./','cogs',f'{Extension}'+ '.py')
    if os.path.exists(extension_path):
        print(f"Extension {Extension} already exist")
        return None
    else:
        with open(extension_path, 'w') as fd:
            fd.write(code.substitute(Extension=Extension))

def remove_extension(Extension: str):
    extension_path = os.path.join('./','cogs',f'{Extension}'+ '.py')
    if os.path.exists(extension_path):
        os.remove(extension_path)
        print(f"Extension {Extension} removed")
    else:
        print(f"Extension {Extension} does not exist!")


def main():
        parser = argparse.ArgumentParser(description= f"Bot manager version {__version__}.")
        parser.add_argument('--new',  nargs='?', default='None', type=str)
        parser.add_argument('--delete',  nargs='?', default='None', type=str)
        config = parser.parse_args()

        if config.new != 'None':
            new_extension(config.new)

        if config.delete != 'None':
            remove_extension(config.delete)
