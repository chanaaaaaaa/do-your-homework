import discord 
from discord.ext import commands
import time
import asyncio
import datetime
from discord.ext import tasks
import datetime
from datetime import timedelta
import json
import os , sys
import asyncio
from discord.ui import Button, View

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='=', intents = intents)

with open('.\setting.json', mode = 'r',encoding="utf8",newline='') as jf :
    output=json.load(jf)

#"科目設定" "全部"為pri預設 無需增加
list1=["國文","英文","數學","物理","化學","生物","地科","地理","歷史","公民","美術","國防","新莊","生命"]
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
async def pr1(ctx,*args):
    
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
    





class button1(Button):
    def __init__(self,label):
        super().__init__(label=label)

    async def callback(self,interaction):
        
        embed=discord.Embed(title="科目",
                            description="你選擇的科目是:"+str(self.label),
                            color=0x109319
                            )
        await interaction.response.edit_message(embed=embed)


        await interaction.channel.send("請輸入科目內容:") 
        await asyncio.sleep(1)
        
        try:
            ins = await bot.wait_for("message", timeout=20)        
        except asyncio.TimeoutError:
            embed=discord.Embed(title="超時",
                                description="操作逾時",
                                color=0xFF5733
                                )
            await interaction.channel.send(embed=embed)
            return

        embed=discord.Embed(title="內容",
                            description="內容為:"+str(ins.content),
                            color=0x109319
                            )
        await interaction.channel.send(embed=embed)


        timeError = True
        await interaction.channel.send("請輸入科目截止時間:")
        await asyncio.sleep(1)
        while timeError == True:

            try:
                timeout = await bot.wait_for("message", timeout=20)
            except asyncio.TimeoutError:
                embed=discord.Embed(title="超時",
                                description="操作逾時",
                                color=0xFF5733
                                )
                await interaction.channel.send(embed=embed)
                return

            try:
                target=time.strftime("%Y-%m-%d",time.strptime(str(timeout.content),"%Y-%m-%d"))
                timeError = False
            except(ValueError):
                embed=discord.Embed(title="錯誤 請重試",
                                    description="日期 為 YYYY-MM-DD",
                                    color=0xFF5733
                                    )
                await interaction.channel.send(embed=embed)

        embed=discord.Embed(title="截止時間",
                            description="截止時間為:"+str(timeout.content),
                            color=0x109319
                            )
        await interaction.channel.send(embed=embed)

        with open('.\setting.json', mode = 'r',encoding="utf-8",newline='') as jf :
            input=json.load(jf)

        try:
            for i in range(1,20):
                print(input[str(self.label)+str(i)])
        except(KeyError):
            pass

        input[str(self.label)+str(i)]=target,str(ins.content),i
        with open('.\setting.json', mode = 'w',encoding="utf-8",newline='') as jf :
            json.dump(input,jf,indent=10,ensure_ascii=False)

        embed=discord.Embed(title="加入",
                            description=(str(self.label)+"科 "+str(timeout.content)+"截止 內容為"+str(ins.content)+" 編號為"+str(i)+" 加入成功!"),
                            color=0x109319
                            )
        await interaction.channel.send(embed=embed)



class button_add(Button):
    def __init__(self,label):
        super().__init__(label=label)

    async def callback(self,interaction):
        
        embed=discord.Embed(title="科目",
                            description="你選擇的科目是:"+str(self.label),
                            color=0x109319
                            )
        await interaction.response.edit_message(embed=embed)


        await interaction.channel.send("請輸入科目內容:") 
        await asyncio.sleep(1)
        
        try:
            ins = await bot.wait_for("message", timeout=20)        
        except asyncio.TimeoutError:
            embed=discord.Embed(title="超時",
                                description="操作逾時",
                                color=0xFF5733
                                )
            await interaction.channel.send(embed=embed)

        embed=discord.Embed(title="內容",
                            description="內容為:"+str(ins.content),
                            color=0x109319
                            )
        await interaction.channel.send(embed=embed)


        timeError = True
        await interaction.channel.send("請輸入科目截止時間:")
        await asyncio.sleep(1)
        while timeError == True:

            try:
                timeout = await bot.wait_for("message", timeout=20)
            except asyncio.TimeoutError:
                embed=discord.Embed(title="超時",
                                description="操作逾時",
                                color=0xFF5733
                                )
                await interaction.channel.send(embed=embed)

            try:
                target=time.strftime("%Y-%m-%d",time.strptime(str(timeout.content),"%Y-%m-%d"))
                timeError = False
            except(ValueError):
                embed=discord.Embed(title="錯誤 請重試",
                                    description="日期 為 YYYY-MM-DD",
                                    color=0xFF5733
                                    )
                await interaction.channel.send(embed=embed)

        embed=discord.Embed(title="截止時間",
                            description="截止時間為:"+str(timeout.content),
                            color=0x109319
                            )
        await interaction.channel.send(embed=embed)


        with open('.\setting.json', mode = 'r',encoding="utf-8",newline='') as jf :
            input=json.load(jf)
        try:
            for i in range(1,20):
                print(input[str(self.label)+str(i)])
        except(KeyError):
            pass

        embed=discord.Embed(title="確認是否加入 超過10秒自動加入",
                            description=(str(self.label)+"科 "+str(timeout.content)+"截止 內容為"+str(ins.content)+" 編號為"+str(i)),
                            color=0x109319
                            )


        button1 = Button(label = "確認")
        async def button_callback(interaction):
            embed=discord.Embed(title="加入成功",
                                description=(str(self.label)+"科 "+str(timeout.content)+"截止 內容為"+str(ins.content)+" 編號為"+str(i)+" 加入成功"),
                                color=0x109319
                                )
            input[str(self.label)+str(i)]=target,str(ins.content),i
            with open('.\setting.json', mode = 'w',encoding="utf-8",newline='') as jf :
                json.dump(input,jf,indent=10,ensure_ascii=False)
            view.remove_item(button1)
            view.remove_item(button2)
            await interaction.response.edit_message(embed=embed , view=view)
            exit
        button1.callback = button_callback

        button2 = Button(label = "取消")
        async def button_callback(interaction):
            embed=discord.Embed(title="取消加入",
                                description="取消成功!",
                                color=0x109319
                                )
            view.remove_item(button1)
            view.remove_item(button2)
            await interaction.response.edit_message(embed=embed , view=view)
            exit
        button2.callback = button_callback

        view = View()
        view.add_item(button1)
        view.add_item(button2)
        await interaction.channel.send(embed=embed , view=view)
        try:
            interaction = await bot.wait_for("button_click", timeout=10)
        except asyncio.TimeoutError:
            embed=discord.Embed(title="加入成功",
                                description=(str(self.label)+"科 "+str(timeout.content)+"截止 內容為"+str(ins.content)+" 編號為"+str(i)+" 加入成功"),
                                color=0x109319
                                )
            await interaction.channel.send(embed=embed)
            exit
        

@bot.command()
async def add(ctx):

    view = View()

    for i in range(len(list1)):
        button = button_add(str(list1[i-1]))
        view.add_item(button)
    await ctx.send("choose",view=view)
    



@bot.command()
async def pri(ctx):

    view = View()

    for i in range(len(list1)):
        button = button_pri(str(list1[i-1]))
        view.add_item(button)

    button = Button(label="全部")
    async def button_callback(interaction):
        embed=discord.Embed(title="科目",
                            description="你選擇的科目是:全部",
                            color=0x109319
                            )
        await interaction.response.edit_message(embed=embed)

        with open('.\setting.json', mode = 'r',encoding="utf-8",newline='') as jf :
            output=json.load(jf)

        embed=discord.Embed(title="全部",
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
        await interaction.channel.send(embed=embed)
        exit
    button.callback = button_callback

    view.add_item(button)

    await ctx.send("choose",view=view)




class button_pri(Button):
    def __init__(self,label):
        super().__init__(label=label)

    async def callback(self,interaction):
        
        embed=discord.Embed(title="科目",
                            description="你選擇的科目是:"+str(self.label),
                            color=0x109319
                            )
        await interaction.response.edit_message(embed=embed)


        with open('.\setting.json', mode = 'r',encoding="utf-8",newline='') as jf :
            output=json.load(jf)

        embed=discord.Embed(title="已選定科目:"+(self.label),
                            description="科目 - 時間 - 內容 - 編號",
                            color=0x109319
                            )
        
        
        for a in range(1,20):
            try:
                embed.add_field(name=str(self.label),
                                value=str(output[str(self.label)+str(a)]),
                                inline=False
                                )
            except(KeyError):
                if a == 1:
                    embed.add_field(name=str(self.label),
                                value="無紀錄",
                                inline=False
                                )
                pass
            except(IndexError):
                pass
        
        await interaction.channel.send(embed=embed)



@bot.command()
async def pr(ctx,*args):
    list1=["國文","英文","數學","物理","化學","生物","地科","地理","歷史","公民","美術","國防","新莊","生命","全部"]
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




bot.run(output["TOKEN"])