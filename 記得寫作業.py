import discord
from discord.ext import commands
import json
import random
import datetime
import asyncio

intents = discord.Intents.all()
intents.members = True

with open('.vscode\setting.json', mode = 'r',encoding="utf8") as jfile :
    jdata = json.load(jfile)

bot = commands.Bot(command_prefix='{', intents = intents)

@bot.event
async def on_ready():
    print("already")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(int(jdata['welcome_channel']))
    await channel.send(f'{member}join!')

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(int(jdata['leave_channel']))
    await channel.send(f'{member}leave!')

@bot.command()
async def ping(ctx):
    await ctx.send(f'{round(bot.latency*1000)}(ms)')

@bot.command()
async def picture(ctx):
    random_pic = random.choice(jdata['pic'])
    pic = discord.File(random_pic)
    await ctx.send(file = pic)

@bot.command()
async def web(ctx):
    random_pic = random.choice(jdata['url_pic'])
    await ctx.send(random_pic)

@bot.command()
async def work(ctx,*,msg):
    await ctx.messsage.delete()
    await ctx.send(msg)

@bot.command()
async def clean(ctx,num : int):
    await ctx.messsage.purge(limit = num + 1)

class Task():
    def __init__(*args,**kwargs):
    
        async def time_task():
            await bot.wait_until_ready()
            channel = bot.get_channel(974513106166382643)
            while not bot.is_closed():
                now_time = datetime.datetime.now().strftime('%m%D')
                with open('.vscode\setting.json','r',encoding='utf8') as jfile :
                   jdata = josn.load(jfile)
                if now_time == jdata['time']:
                    await channel.send('Task working')
                    await asyncio.sleep(1)
                else :
                    asyncio.sleep(1)
                    pass

        bg_task = bot.loop.creat_task(time_task())

@bot.command()
async def c(ctx,time):
    with open('.vscode\setting.json','r',encoding='utf8') as jfile :
        jdata = json.load(jfile)
    jdata['time'] = time
    with open('.vscode\setting.json','w',encoding='utf8') as jfile :
        json.dump(jdata,jfile,indent=4)

bot.run(jdata['TOKEN'])