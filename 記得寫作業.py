import discord
From discord.ext import commands

bot = commands.Bot(command_prefix='+')

@bot.event
async deF on_ready():
    print(">>bot is online <<")

bot.run('MTAyMzkwOTEwOTIyMjg4NzQ5NQ.GbYThN.SacgsmY4xMk0W8o0ARrWcgIRhbibVO-HNa4_x8')