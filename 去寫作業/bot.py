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
async def createcc(ctx,name):
    guild = ctx.guild
    await guild.create_text_channel("{}".format(name))
    


   





@commands.has_permissions(administrator=True)
@bot.command()
async def create_new_channel(ctx, channel_name: str):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    admin_role = guild.get_role(956252661970247840)
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=True),
        ctx.author: discord.PermissionOverwrite(view_channel=True),
        admin_role: discord.PermissionOverwrite(view_channel=True),
        guild.me: discord.PermissionOverwrite(view_channel=True)
    }
    if not existing_channel:
        await guild.create_text_channel(channel_name ,overwrites=overwrites)
        await ctx.send(f'Channel {channel_name} has been created!')
    else:
        await ctx.send(f'Channel {channel_name} already exists!')




@bot.command()
async def create_channel(ctx, channel_name: str):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        await guild.create_text_channel(channel_name)
        await ctx.send(f'成功：{channel_name}')





@bot.command()
async def date(ctx):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    message = f"今天是 {today}"
    await ctx.send(message)





bot.run(jdata['TOKEN'])