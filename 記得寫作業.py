import discord
from discord.ext import commands
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='+', intents = intents)

@bot.event
async def on_ready():
    print(">> Bot is online <<")

@bot.event
async def on_member_join(member):
    print(f'{member}join!')

@bot.event
async def on_member_remove(member):
    print(f'{member}leave!')


bot.run('MTAyMzkwOTEwOTIyMjg4NzQ5NQ.G1yyjB.jO9t0tA_jIybr_MnNyif_4ngidTswMPukk929k')