import discord 
from discord.ext import commands
import json
import time
import datetime
from discord.ext import tasks

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='=', intents = intents)

with open('.\setting.json', mode = 'r',encoding="utf8",newline='') as jf :
        jdata=json.load(jf)

#"科目":"國文","英文","數學","物理","化學","地理","歷史","公民","美數","國防","新莊學"

@bot.event
async def on_ready():
    print("機器啟動")



@bot.command()
async def hi(ctx):
    await ctx.send('hi')

@bot.command()
async def tr(ctx):
        await ctx.send(jdata['國文1'][1])





@bot.command()
async def 國文入(ctx,timein,ins): #=schedulein 年-月-日 內容
    with open('.\setting.json', mode = 'r',encoding="utf-8",newline='') as jf :
        input=json.load(jf)
        target=time.strftime("%Y-%m-%d",time.strptime(timein,"%Y-%m-%d"))
        input["國文"]=target,(ins)
    with open('.\setting.json', mode = 'w',encoding="utf-8",newline='') as jf :
        json.dump(input,jf,ensure_ascii=False)
    await ctx.send("done")

@bot.command()
async def date(ctx):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    message = f"今天是 {today}"
    await ctx.send(message)





bot.run(jdata["TOKEN"])