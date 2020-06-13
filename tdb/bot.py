import dotenv
import os
from discord.ext import commands
from tdb import logger

class Main() :
    def __init__(self):
        load_dotenv(os.path('./'))
        self.Log = logger.GetLogger('logs', __name__)
        self.Log.info("version v.0.0.1")
        self.config = dict(token=os.getenv('DEVELOP_TOKEN'))
        self.Log.info("Token Loaded.")
        self.bot = commands.Bot(command_prefix='.')
        self.load_extensions()

    def load_extensions(self):
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

    def run(self):
        try:
            self.bot.run(self.config['token'])
        except Exception as e:
            self.Log.info(e)

if __name__ == '__main__':
    main = Main()
    main.run()
