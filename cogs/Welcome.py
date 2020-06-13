from discord.ext.commands import Cog
from discord.ext import commands
from datetime import datetime

class Welcome(Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome {member.mention} to the best Warzone Tournament Bot for the moment {datetime.now()}.')

    @commands.command()
    async def hello(self, ctx, *args):
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'Hi {member.name}')
        else:
            await ctx.send(f'Hi again {member.name}!')
            self._last_member = member

def setup(bot):
    bot.add_cog(Welcome(bot))
