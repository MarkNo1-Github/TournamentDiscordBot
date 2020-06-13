from dotenv import load_dotenv
import os
from discord.ext import commands


print("Bot Tournament Discord:  version v.0.0.1")

load_dotenv()
config = dict(token=os.getenv('DEVELOP_TOKEN'))
print("Bot Tournament Discord:  Token Loaded.")

bot = commands.Bot(command_prefix='.')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        print(f'Bot Tournament Discord:  Loading {filename}.')
        bot.load_extension(f'cogs.{filename[:-3]}')

print("Bot Tournament Discord:  Extensions Loaded.")
try:
    bot.run(config['token'])
except Exception as e:
    print(e)
