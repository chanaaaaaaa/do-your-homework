import discord 
from discord.ext import commands
import time
import asyncio
import datetime
from discord.ext import tasks
import datetime
from datetime import timedelta
import json
import os
import asyncio
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='=', intents=intents)

with open('.\setting.json', mode='r', encoding="utf8", newline='') as jf:
    output = json.load(jf)

@bot.event
async def on_ready():
    print("機器啟動")

@bot.command()
async def pr(ctx):
    list1 = ["國文", "英文", "數學", "物理", "化學", "生物", "地科", "地理", "歷史", "公民", "美術", "國防", "新莊", "生命"]
    embed = discord.Embed(title="行程清單", description="請選擇科目：", color=0x109319)
    for subject in list1:
        embed.add_field(name=subject, value=subject, inline=False)
    message = await ctx.send(embed=embed)
    for subject in list1:
        await message.add_reaction(subject)

@bot.command()
async def add(ctx):
    list1 = ["國文", "英文", "數學", "物理", "化學", "生物", "地科", "地理", "歷史", "公民", "美術", "國防", "新莊", "生命"]
    embed = discord.Embed(title="新增行程", description="請選擇科目：", color=0x109319)
    for subject in list1:
        embed.add_field(name=subject, value=subject, inline=False)
    message = await ctx.send(embed=embed)
    for subject in list1:
        await message.add_reaction(subject)

@bot.command()
async def delete(ctx):
    list1 = ["國文", "英文", "數學", "物理", "化學", "生物", "地科", "地理", "歷史", "公民", "美術", "國防", "新莊", "生命"]
    embed = discord.Embed(title="刪除行程", description="請選擇科目：", color=0x109319)
    for subject in list1:
        embed.add_field(name=subject, value=subject, inline=False)
    message = await ctx.send(embed=embed)
    for subject in list1:
        await message.add_reaction(subject)

@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user:
        return
    if isinstance(reaction.message.channel, discord.DMChannel):
        return
    if str(reaction.emoji) in ["國文", "英文", "數學", "物理", "化學", "生物", "地科", "地理", "歷史", "公民", "美術", "國防", "新莊", "生命"]:
        subject = str(reaction.emoji)
        await reaction.message.delete()
        if reaction.message.content.startswith('=pr'):
            await show_schedule(reaction.message.channel, subject)
        elif reaction.message.content.startswith('=add'):
            await add_schedule(reaction.message.channel, subject)
        elif reaction.message.content.startswith('=delete'):
            await delete_schedule(reaction.message.channel, subject)

async def show_schedule(channel, subject):
    # 根据所选的科目显示相应的行程
    # 您的代码...

async def add_schedule(channel, subject):
    # 根据所选的科目添加行程
    # 您的代码...

async def delete_schedule(channel, subject):
    # 根据所选的科目删除行程
    # 您的代码...

bot.run(output["TOKEN"])