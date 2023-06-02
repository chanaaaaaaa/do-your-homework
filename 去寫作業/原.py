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
    list1=["國文","英文","數學","物理","化學","生物","地科","地理","歷史","公民","美術","國防","新莊","生命"]
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

                    embed=discord.Embed(title="刪除",
                            description=f"項目 {list1[a]} 編號{i} 已過期，已自動刪除",
                            color=0xFF5733
                            )      
                    await bot.get_channel(output["channelID"]).send(embed=embed)

        except Exception as e:
            print(f"處理項目 {list1[a]} 時發生錯誤：{e}")

    await asyncio.sleep(10)



@bot.command()
async def idget(ctx):
    embed=discord.Embed(title="成功",
                        description="取得成功",
                        color=0x109319
                        )
    await ctx.send(embed=embed)
    output["channelID"]= ctx.channel.id

    with open('.\setting.json', mode = 'w',encoding="utf-8",newline='') as jf :
        json.dump(output,jf,indent=10,ensure_ascii=False)



@bot.command()
async def hi(ctx):

    if output["channelID"] == "" :
        embed=discord.Embed(title="提醒",
                            description="記得要設定頻道ID!",
                            color=0xFF5733
                            )
        await ctx.send(embed=embed)

    embed=discord.Embed(title="成功",
                            description="測試成功",
                            color=0xFF5733
                            )
    await ctx.send(embed=embed)



@bot.command()
async def add(ctx,*args): #=schedulein 年-月-日 內容
    with open('.\setting.json', mode = 'r',encoding="utf-8",newline='') as jf :
        input=json.load(jf)

        if input["channelID"] == "" :
            embed=discord.Embed(title="提醒",
                                description="記得要設定頻道ID!",
                                color=0xFF5733
                                )
            await ctx.send(embed=embed)

        if len(args) !=3:
            embed=discord.Embed(title="錯誤",
                                description="輸入格式為 年-月-日 科目 內容",
                                color=0xFF5733
                                )
            await ctx.send(embed=embed)
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

                    embed=discord.Embed(title="成功",
                                        description= str(sub)+" "+str(ins)+" 加入成功 編號為:"+str(i),
                                        color=0x109319
                                        )
                    await ctx.send(embed=embed)

                except(ValueError):
                    embed=discord.Embed(title="錯誤",
                                        description="日期 為 YYYY-MM-DD",
                                        color=0xFF5733
                                        )
                    await ctx.send(embed=embed)
            else:
                embed=discord.Embed(title="錯誤",
                                    description="科目為 國文or英文or數學or物理or化學or生物or地科or地理or歷史or公民or美術or國防or新莊or生命"+"\n格式為 時間 科目 內容",
                                    color=0xFF5733
                                    )
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="錯誤",
                                    description="科目為 國文or英文or數學or物理or化學or生物or地科or地理or歷史or公民or美術or國防or新莊or生命"+"\n格式為 時間 科目 內容",
                                    color=0xFF5733
                                    )
            await ctx.send(embed=embed)



@bot.command()
async def pr(ctx,*args):
    list1=["國文","英文","數學","物理","化學","生物","地科","地理","歷史","公民","美術","國防","新莊","生命"]
    list2=["","","","","","","","","","","","","",""]
    with open('.\setting.json', mode = 'r',encoding="utf-8",newline='') as jf :
        output=json.load(jf)

        if output["channelID"] == "" :
            embed=discord.Embed(title="提醒",
                                description="記得要設定頻道ID!",
                                color=0xFF5733
                                )
            await ctx.send(embed=embed)

    if len(args) == 0:

        embed=discord.Embed(title="全部行程",
                            description="科目 - 時間 - 內容 - 編號",
                            color=0x109319
                            )

        for i in range(0,len(list1)-1):
            try:
                for a in range(1,20):
                    try:
                        embed.add_field(name=str(list1[i]),
                                        value=str(output[list1[i]+str(a)]),
                                        inline=False
                                        )
                    except(KeyError):
                        pass
            except(KeyError):
                continue
        await ctx.send(embed=embed)

    else:

        embed=discord.Embed(title="已選定行程",
                            description="科目 - 時間 - 內容 - 編號",
                            color=0x109319
                            )

        for i in range(0,len(list1)-1):
            try:
                list2[i]=args[i]
            except(IndexError):
                pass
        for i in range(0,len(list2)):
            try:
                for a in range(1,20):
                    try:
                        embed.add_field(name=str(list2[i]),
                                        value=str(output[list2[i]+str(a)]),
                                        inline=False
                                        )
                    except(KeyError):
                        pass
                    except(IndexError):
                        pass
            except(KeyError):
                continue
        await ctx.send(embed=embed)   



@bot.command()
async def delete(ctx,*args): # =刪...... 奇數項為科目 偶數項為代號
    list1=["國文","英文","數學","物理","化學","生物","地科","地理","歷史","公民","美術","國防","新莊","生命"]
    list2=["","","","","","","","","","","","","",""]
    with open('.\setting.json', mode = 'r',encoding="utf-8",newline='') as jf :
        output=json.load(jf)

    if output["channelID"] == "" :
        embed=discord.Embed(title="提醒",
                            description="記得要設定頻道ID!",
                            color=0xFF5733
                            )
        await ctx.send(embed=embed)

    if len(args) == 0:
        embed=discord.Embed(title="錯誤",
                            description="你想刪除什麼",
                            color=0xFF5733
                            )
        await ctx.send(embed=embed)
    if len(args)%2 != 0:
        embed=discord.Embed(title="錯誤",
                            description="想要刪除的項目編號呢",
                            color=0xFF5733
                            )
        await ctx.send(embed=embed)
    if len(args) >= 14:
        embed=discord.Embed(title="錯誤",
                            description="超出上限",
                            color=0xFF5733
                            )
        await ctx.send(embed=embed)
        return

    else:
        for i in range(0,len(args)):
            try:
                list2[i]=args[i]
            except(IndexError):
                pass
        try:
            for i in range(0,len(list2)+2,2):
                if list2[i] not in list1 and list2[i] != "" :
                    embed=discord.Embed(title="錯誤",
                                        description=list2[i]+" 科目錯誤"+"\n科目為 國文or英文or數學or物理or化學or生物or地科or地理or歷史or公民or美術or國防or新莊or生命",
                                        color=0xFF5733
                                        )
                    await ctx.send(embed=embed)
                    continue

                if (str(list2[i])+str(list2[i+1])) in output :
                    del output[str(list2[i])+str(list2[i+1])]
                    embed=discord.Embed(title="成功",
                                        description=str(list2[i])+str(list2[i+1])+" 刪除成功",
                                        color=0x109319
                                        )
                    await ctx.send(embed=embed)                    
                    with open('.\setting.json', mode = 'w',encoding="utf-8",newline='') as jf :
                        json.dump(output,jf,indent=10,ensure_ascii=False)
                        continue  
                if (str(list2[i])+str(list2[i+1])) not in output and list2[i] != "" :
                    embed=discord.Embed(title="錯誤",
                                        description=list2[i]+str(list2[i])+str(list2[i+1])+" 不存在",
                                        color=0xFF5733
                                        )
                    await ctx.send(embed=embed)
                    continue                            
        except(IndexError):
            pass
    

#@bot.command()
#async def settime(ctx,time1):

#    if output["channelID"] == "" :
#        await ctx.send("記得要設定一個頻道讓機器人發送定時訊息喔")
#    if time1 == ():
#        await ctx.send("此命令用意為")
#    with open('.\setting.json', mode = 'r',encoding="utf-8",newline='') as jf :
#        input=json.load(jf)
#    try:
#        input["time"]=time.strftime("%H",time.strptime(time1,"%H"))
#        with open('.\setting.json', mode = 'w',encoding="utf-8",newline='') as jf :
#            json.dump(input,jf,indent=10,ensure_ascii=False)
#        await ctx.send("時間設定完成 為"+ time1 +"時")
#    except(ValueError):
#        await ctx.send("僅需輸入小時 24小時制")




bot.run(output["TOKEN"])