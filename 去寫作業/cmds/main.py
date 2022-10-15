import discord
from discord.ext import commands

class Main(commands.Cog):

    def __init__(self,bot):
        self.bot=bot

    with open('.\pic\setting.json', mode = 'r',encoding="utf8") as jfile :
        jdata = json.load(jfile)
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("already")

    @commands.command()
    async def ping(self,ctx):
        await ctx.send('Pong')
    
def setup(bot):
    bot.add_cog(Main(bot))
