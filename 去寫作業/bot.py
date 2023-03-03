import discord
from discord.ext import commands
import json
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

@bot.command()
async def channel(ctx):
    await guild.creat_text_channel('測試',category=None)

@bot.command()
async def delete(ctx, channel: discord.TextChannel):
    if ctx.author.guild.permissions.manage_channles:
        await ctx.send.invoke(f"Deleted a channel named {name}")
        await channel.delete()
    else:
       await ctx.send('Sorry, but you have a wrong name. Try again, but do it like this: >delete [channel name]') 

@bot.command()
async def create(ctx, *, name=None):
  guild = ctx.message.guild
  if name == None:
    await ctx.send('Sorry, but you have to insert a name. Try again, but do it like this: >create [channel name]')
  else:
    await guild.create_text_channel(name)
    await ctx.send(f"Created a channel named {name}")

bot.run(jdata['TOKEN'])