import discord 
from discord.ext import commands
import time
import datetime
from discord.ext import tasks

import json

import os,sys

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='=', intents = intents)

with open('.\setting.json', mode = 'r',encoding="utf8",newline='') as jf :
        jdata=json.load(jf)

#"科目":"科目為 國文or英文or數學or物理or化學or生物or地科or地理or歷史or公民or美術or國防or新莊or生命

@bot.event
async def on_ready():
    print("機器啟動")

@bot.command()
async def hi(ctx):
    await ctx.send('hi')

@bot.command()
async def 入(ctx,*args): #=schedulein 年-月-日 內容
    with open('.\setting.json', mode = 'r',encoding="utf-8",newline='') as jf :
        input=json.load(jf)
        if len(args) !=3:
            await ctx.send("輸入格式為 年-月-日 科目 內容")
            return
        timein=args[0]
        sub=args[1]
        ins=args[2]
        if "國文"or"英文"or"數學"or"物理"or"化學"or"生物"or"地科"or"地理"or"歷史"or"公民"or"美術"or"國防"or"生命"or"新莊"in sub:
            if len(sub)==2:
                try:
                    for i in range(1,20):
                        print(input[sub+str(i)])
                except(KeyError):
                    pass
                try:
                    target=time.strftime("%Y-%m-%d",time.strptime(timein,"%Y-%m-%d"))
                    input[sub+str(i)]=target,(ins)
                    with open('.\setting.json', mode = 'w',encoding="utf-8",newline='') as jf :
                        json.dump(input,jf,indent=10,ensure_ascii=False)
                    await ctx.send("done")
                except(ValueError):
                    await ctx.send("日期 為 YYYY-MM-DD")
            else:
                await ctx.send("科目為 國文or英文or數學or物理or化學or生物or地科or地理or歷史or公民or美術or國防or新莊or生命")
        else:
            await ctx.send("科目為 國文or英文or數學or物理or化學or生物or地科or地理or歷史or公民or美術or國防or新莊or生命")

@bot.command()
async def 出(ctx,*args):
    list1=["國文","英文","數學","物理","化學","生物","地科","地理","歷史","公民","美術","國防","新莊","生命"]
    list2=["","","","","","","","","","","","","",""]
    with open('.\setting.json', mode = 'r',encoding="utf-8",newline='') as jf :
        output=json.load(jf)
    if len(args) == 0:
        for i in range(0,len(list1)-1):
            try:
                for a in range(1,20):
                    try:
                        await ctx.send(str(list1[i])+":"+str(output[list1[i]+str(a)]))
                    except(KeyError):
                        pass
            except(KeyError):
                continue
    else:
        for i in range(0,len(list1)-1):
            try:
                list2[i]=args[i]
            except(IndexError):
                pass
        for i in range(0,len(list2)+1):
            try:
                for a in range(1,20):
                    try:
                        await ctx.send(str(list2[i])+":"+str(output[list2[i]+str(a)]))
                    except(KeyError):
                        pass
                    except(IndexError):
                        pass
            except(KeyError):
                continue
    list2.clear()






@bot.command()
async def tr(ctx,sub):
    with open('.\setting.json', mode = 'r',encoding="utf-8",newline='') as jf :
        input=json.load(jf)
    for i in range(1,20):
        print(input[sub+str(i)])




@bot.command()
async def date(ctx):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    message = f"今天是 {today}"
    await ctx.send(message)


bot.run(jdata["TOKEN"])