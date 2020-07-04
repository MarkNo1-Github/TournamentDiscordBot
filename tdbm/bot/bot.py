import dotenv
from pathlib import Path
from discord.ext import commands
from tdbm.logger import Logger


class Main(Logger) :
    def __init__(self, config):
        super().__init__("Bot")
        self(debug=f"Started")
        self.config = config
        self.bot = commands.Bot(command_prefix='.')
        self.path = Path("./").absolute()
        self.extensions_path = self.path / "cogs"
        self.load_extensions()

    def load_extensions(self):
        self(debug="Loading Extensions")
        self(debug=f"Path:{self.path}")
        if self.extensions_path.exists():
            for file in  self.extensions_path.iterdir():
                filename = file.name
                if filename.endswith('.py'):
                    self(info=f'Loading extension: {filename}.')
                    self.bot.load_extension(f'cogs.{filename[:-3]}')
            self(info="Extensions Loaded.")
        else:
            self(error="No Cogs Extensions folder")
        self(debug="Extensions all loaded")

    def run(self):
        try:
            self.bot.run(self.config['token'])
        except Exception as e:
            self.Log.info(e)
