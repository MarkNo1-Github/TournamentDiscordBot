import dotenv
import os
from discord.ext import commands
from tdbm import logger


class Main() :
    def __init__(self, config):
        self.Log = logger.GetFileLogger('logs', __name__)
        self.Log.info(f"Started")
        self.config = config
        self.bot = commands.Bot(command_prefix='.')
        self.load_extensions()

    def load_extensions(self):
        self.Log.info("Start")
        print('current paht', os.path.abspath('./'))
        extension_folder = os.path.join(os.path.abspath('./'), 'cogs')
        if os.path.exists(extension_folder):
            for filename in os.listdir(extension_folder):
                if filename.endswith('.py'):
                    self.Log.info(f'Loading extension: {filename}.')
                    self.bot.load_extension(f'cogs.{filename[:-3]}')
            self.Log.info("Extensions Loaded.")
        else:
            self.Log.error("No Cogs Extensions folder")
        self.Log.info("End")

    def run(self):
        try:
            self.bot.run(self.config['token'])
        except Exception as e:
            self.Log.info(e)
