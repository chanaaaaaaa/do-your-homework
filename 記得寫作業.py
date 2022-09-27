import discord
from discord.ext import commands

bot = commands.Bot(command_orefix='sd')

@bot.event
async def on_ready():
    print(">> Bot is online <<")

bot.run('MTAyMzkwOTEwOTIyMjg4NzQ5NQ.GlHNp0.02Mc9jYOGfDUyZ5Y2i_urrtvvQvhzi9Li9re6Y')