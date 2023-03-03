import discord 
from discord.ext import commands
import json
import asyncio
import datetime
from discord import Guild, TextChannel
from discord.ext import tasks
import asyncio


with open('.\setting.json', mode = 'r',encoding="utf8") as jfile :
    jdata = json.load(jfile)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='=', intents = intents)

@bot.event
async def on_ready():
    print("機器啟動")

@bot.event
async def member_in(name):
    await on_message(name)

@bot.command()
async def hi(ctx):
    await ctx.send('hi')

@commands()
async def schedulein(ctx,time,obj,range):
    




@bot.command()
async def date(ctx):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    message = f"今天是 {today}"
    await ctx.send(message)





bot.run(jdata['TOKEN'])