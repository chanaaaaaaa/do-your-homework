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
list1=["國文","英文","數學","物理","化學","生物","地科","地理","歷史","公民","美術","國防","新莊","生命"]
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='=', intents = intents)

with open('.\setting.json', mode = 'r',encoding="utf8",newline='') as jf :
    output=json.load(jf)

#"科目":"科目為 國文or英文or數學or物理or化學or生物or地科or地理or歷史or公民or美術or國防or新莊or生命
@bot.event
async def on_ready():
    now = datetime.datetime.now()
    print(now)
    check_expired_items3.start()
    print("機器啟動")

@tasks.loop(minutes=60)
async def check_expired_items3():
    now = datetime.datetime.now()

    for a in range(0, len(list1)-1):
        try:
            for i in range(1, 20):
                item = output.get(str(list1[a])+str(i))
                if not item:
                    continue
                
                tim = item[0]
                ins = item[1]
                num = item[2]

                try:
                    tim = datetime.datetime.strptime(tim, "%Y-%m-%d")
                except ValueError:
                    continue

                if (now - tim).days >= 14:
                    del output[str(list1[a])+str(i)]
                    with open("setting.json", "w", encoding="utf8") as jf:
                        json.dump(output, jf, ensure_ascii=False)
                    print(f"項目 {list1[a]}{i} 已過期，已自動刪除")
                    await check_expired_items3.send(f"項目 {list1[a]}{i} 已過期，已自動刪除")
        except Exception as e:
            print(f"處理項目 {list1[a]} 時發生錯誤：{e}")


@tasks.loop(minutes=60)
async def check_expired_items1():
    now = datetime.date.today()# 取得現在時間
    
    for a in range(0,len(output)-1):
    
        try:
            for i in range(1,20):
                tim=output[str(list1[a])+str(i)][0]
                tim=time.strptime(tim,"%Y-%m-%d")
                ins=output[str(list1[a])+str(i)][1]
                num=output[str(list1[a])+str(i)][2]

                if (now - time).days >=14:
                    del output[str(list1[a])+str(i)]
                    with open("setting.json", "w", encoding="utf8") as jf:
                        json.dump(output, jf, ensure_ascii=False)
                    print("項目"+ str(list1[a])+str(i) +" 已過期，已自動刪除")

        except(KeyError):
            continue
        except(ValueError):    
            continue







list1=["國文","英文","數學","物理","化學","生物","地科","地理","歷史","公民","美術","國防","新莊","生命"]
#2元陣列召喚
#解碼target
@tasks.loop(minutes=60)
async def check_expired_items():
    now = datetime.datetime.now()# 取得現在時間

    for a in range(0,len(list1)-1):
    
        try:
            for i in range(1,20):
                tim=output[str(list1[a])+str(i)][0]
                tim=time.strptime(tim,"%Y-%m-%d")
                ins=output[str(list1[a])+str(i)][1]
                num=output[str(list1[a])+str(i)][2]

                if (now - tim).days >=14:
                    del output[str(list1[a])+str(i)]
                    with open("setting.json", "w", encoding="utf8") as jf:
                        json.dump(output, jf, ensure_ascii=False)
                    print("項目"+ str(list1[a])+str(i) +" 已過期，已自動刪除")

        except(KeyError):
            continue
        except(ValueError):    
            continue
    

@bot.command()
async def hi(ctx):
    timeout=datetime.datetime.now()
    timeout=time.strftime("%Y-%m-%d",timeout)
    timeout=time.strptime(timeout,"%Y-%m-%d")
    await ctx.send(timeout)

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
                    input[sub+str(i)]=target,(ins),i
                    with open('.\setting.json', mode = 'w',encoding="utf-8",newline='') as jf :
                        json.dump(input,jf,indent=10,ensure_ascii=False)
                    await ctx.send(str(sub)+" "+str(ins)+" 加入成功 編號為:"+str(i))
                except(ValueError):
                    await ctx.send("日期 為 YYYY-MM-DD")
            else:
                await ctx.send("科目為 國文or英文or數學or物理or化學or生物or地科or地理or歷史or公民or美術or國防or新莊or生命"+"\n格式為 時間 科目 內容")
        else:
            await ctx.send("科目為 國文or英文or數學or物理or化學or生物or地科or地理or歷史or公民or美術or國防or新莊or生命"+"\n格式為 時間 科目 內容")

@bot.command()
async def 出(ctx,*args):
    list1=["國文","英文","數學","物理","化學","生物","地科","地理","歷史","公民","美術","國防","新莊","生命"]
    list2=["","","","","","","","","","","","","",""]
    with open('.\setting.json', mode = 'r',encoding="utf-8",newline='') as jf :
        output=json.load(jf)
    await ctx.send("科目 時間                   內容        編號")
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
        for i in range(0,len(list2)):
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

@bot.command()
async def 刪(ctx,*args): # =刪...... 奇數項為科目 偶數項為代號
    sbjError=False
    list1=["國文","英文","數學","物理","化學","生物","地科","地理","歷史","公民","美術","國防","新莊","生命"]
    list2=["","","","","","","","","","","","","",""]
    with open('.\setting.json', mode = 'r',encoding="utf-8",newline='') as jf :
        output=json.load(jf)
    if len(args) == 0:
        await ctx.send("你想刪除什麼")
    if len(args)%2 != 0:
        await ctx.send("是不是漏了什麼")
    else:
        for i in range(0,len(args)):
            try:
                list2[i]=args[i]
            except(IndexError):
                pass
        try:
            for i in range(0,len(list2)+2,2):
                if list2[i] not in list1 and list2[i] != "" :
                    await ctx.send(list2[i]+" 科目錯誤")
                    sbjError=True
                    continue
                if (str(list2[i])+str(list2[i+1])) in output :
                    del output[str(list2[i])+str(list2[i+1])]
                    await ctx.send(str(list2[i])+str(list2[i+1])+" 刪除成功")
                    with open('.\setting.json', mode = 'w',encoding="utf-8",newline='') as jf :
                        json.dump(output,jf,indent=10,ensure_ascii=False)
                        continue  
                if (str(list2[i])+str(list2[i+1])) not in output and list2[i] != "" :
                    await ctx.send(str(list2[i])+str(list2[i+1])+" 不存在")
                    continue                            
        except(IndexError):
            pass
    if sbjError == True :
        await ctx.send("科目為 國文or英文or數學or物理or化學or生物or地科or地理or歷史or公民or美術or國防or新莊or生命")



async def time_task():
    counter = 0
    channel=bot.get_channel(974513106166382643)#########
    await bot.wait_until_ready()
    while not bot.is_closed():
        now=datetime.datetime.now().strftime("%H")
        with open('.\setting.json', mode = 'r',encoding="utf-8",newline='') as jf :
            input=json.load(jf)
        if now == input["time"] and counter == 0 :
            await channel.send("今天應交功課")
            counter = 1
        else:
            await asyncio.sleep(1)
            counter = 0
            pass

@bot.command()
async def 設定時間(ctx,time1):
    with open('.\setting.json', mode = 'r',encoding="utf-8",newline='') as jf :
        input=json.load(jf)
    try:
        input["time"]=time.strftime("%H",time.strptime(time1,"%H"))
        with open('.\setting.json', mode = 'w',encoding="utf-8",newline='') as jf :
            json.dump(input,jf,indent=10,ensure_ascii=False)
        await ctx.send("時間設定完成 為"+ time1 +"時")
    except(ValueError):
        await ctx.send("僅需輸入小時 24小時制")




bot.run(output["TOKEN"])