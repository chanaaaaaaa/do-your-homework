import discord
from discord.ext import commands
import json
import os

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='=', intents = intents)

with open('.\pic\setting.json', mode = 'r',encoding="utf8") as jfile :
    jdata = json.load(jfile)

@bot.command()
async def load(ctx,extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command()
async def unload(ctx,extension):
    bot.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cmds'):
    if filename.endswith('.py'):
        bot.load_extension(f"cmds.{filename[:-3]}")


if __name__=="__main__":
    bot.run(jdata['TOKEN'])