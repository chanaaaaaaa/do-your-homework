import discord
from discord.ext import commands
intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='{', intents = intents)

@bot.event
async def on_ready():
    print("already")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1024318169483071558)
    await channel.send(f'{member}join!')

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1024318188504240178)
    await channel.send(f'{member}leave!')

@bot.command()
async def ping(ctx):
    await ctx.send(f'{round(bot.latency*1000)}(ms)')

bot.run('MTAyMzkwOTEwOTIyMjg4NzQ5NQ.G1yyjB.jO9t0tA_jIybr_MnNyif_4ngidTswMPukk929k')