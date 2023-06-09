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

    output["channelID"] =" "

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
async def hello(ctx):
    embed=discord.Embed(title="主頁",
                        description="這是一個目的為替代聯絡簿的機器人",
                        color=0x109319
                        )
    embed.set_author(name="吳瑞宸 盧宣嘉")

    if output["channelID"] == "" :
        embde.add_field(name="提醒",
                        value="記得要設定頻道ID!",
                        inline=False
                        )

    view = View()

    button1 = button_idget("idget")
    button2 = button_add_add("add",discord.ButtonStyle.green)
    button3 = button_pri_add("pri",discord.ButtonStyle.blurple)
    button4 = button_del_add("del",discord.ButtonStyle.red)

    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)
    view.add_item(button4)

    await ctx.send(embed=embed , view=view)


class button_idget(Button):
    def __init__(self,label):
        super().__init__(label=label)

    async def callback(self,interaction):
        embed=discord.Embed(title="成功",
                            description="取得成功",
                            color=0x109319
                            )

        output["channelID"]= interaction.channel.id

        with open('.\setting.json', mode = 'w',encoding="utf-8",newline='') as jf :
            json.dump(output,jf,indent=10,ensure_ascii=False)

        await interaction.response.send_message(embed=embed)

    

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
                            description=(str(self.label)+"科 "+str(timeout.content)+"截止 內容為"+str(ins.content)),
                            color=0x109319
                            )

        button1 = Button(label = "確認")
        async def button_callback(interaction):
            embed=discord.Embed(title="加入成功",
                                description=(str(self.label)+"科 "+str(timeout.content)+"截止 內容為"+str(ins.content)+" 加入成功"),
                                color=0x109319
                                )
            input[str(self.label)+str(i)]=target,str(ins.content)
            with open('.\setting.json', mode = 'w',encoding="utf-8",newline='') as jf :
                json.dump(input,jf,indent=10,ensure_ascii=False)
            view.remove_item(button1)
            view.remove_item(button2)
            await interaction.response.edit_message(embed=embed , view=view)
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
        button2.callback = button_callback

        view = View()
        view.add_item(button1)
        view.add_item(button2)
        await interaction.channel.send(embed=embed , view=view)
        try:
            interaction = await bot.wait_for("button_click", timeout=10)
        except(asyncio.TimeoutError):
            try:
                embed=discord.Embed(title="加入成功",
                                    description=(str(self.label)+"科 "+str(timeout.content)+"截止 內容為"+str(ins.content)+" 加入成功"),
                                    color=0x109319
                                    )
                view.remove_item(button1)
                view.remove_item(button2)
                await interaction.response.edit_message(embed=embed , view=view)
                input[str(self.label)+str(i)]=target,str(ins.content)
                with open('.\setting.json', mode = 'w',encoding="utf-8",newline='') as jf :
                    json.dump(input,jf,indent=10,ensure_ascii=False)
            except(discord.errors.InteractionResponded):
                return
             
class button_add_add(Button):
    def __init__(self,label,style):
        super().__init__(label=label,style=style)

    async def callback(self,interaction):

        view = View()

        for i in range(len(list1)):
            button = button_add(str(list1[i-1]))
            view.add_item(button)
        await interaction.response.send_message("choose",view=view)



class button_pri_add(Button):
    def __init__(self,label,style):
        super().__init__(label=label,style=style)

    async def callback(self,interaction):

        view = View()

        for i in range(len(list1)):
            button = button_pri(str(list1[i-1]))
            view.add_item(button)

        button = Button(label="全部")
        async def button_callback(interaction):

            with open('.\setting.json', mode = 'r',encoding="utf-8",newline='') as jf :
                output=json.load(jf)
            
            embed=discord.Embed(title="全部",
                                description="科目\n時間 - 內容",
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
            await interaction.response.send_message(embed=embed)
            exit
        button.callback = button_callback

        view.add_item(button)

        await interaction.response.send_message("choose",view=view)

class button_pri(Button):
    def __init__(self,label):
        super().__init__(label=label)

    async def callback(self,interaction):
    
        with open('.\setting.json', mode = 'r',encoding="utf-8",newline='') as jf :
            output=json.load(jf)

        embed=discord.Embed(title="已選定科目:"+(self.label),
                            description="科目\n時間 - 內容",
                            color=0x109319
                            )
        
        a = 0
        for a in range(1,20):
            try:
                embed.add_field(name=str(self.label),
                                value=str(output[str(self.label)+str(a)]),
                                inline=False
                                )
                a=a+1
            except(KeyError):
                if a == 0:
                    embed.add_field(name=str(self.label),
                                value="無紀錄",
                                inline=False
                                )
                pass
            except(IndexError):
                pass
        
        await interaction.response.send_message(embed=embed)
        

class button_del_add(Button):
    def __init__(self,label,style):
        super().__init__(label=label,style=style)

    async def callback(self,interaction):

        view = View()

        with open('.\setting.json', mode = 'r',encoding="utf-8",newline='') as jf :
            output=json.load(jf)

        for i in range(len(list1)):
            for a in range(1,20):
                try:
                    button = button_del(str(list1[i])+str(output[list1[i]+str(a)]))
                    view.add_item(button)
                except (KeyError) :
                    pass
                except (IndexError):
                    pass

        await interaction.response.send_message("choose",view=view)

class button_del(Button):
    def __init__(self,label):
        super().__init__(label=label)

    async def callback(self,interaction):

        with open('.\setting.json', mode = 'r',encoding="utf-8",newline='') as jf :
            output=json.load(jf)

        embed=discord.Embed(title="確認是否刪除 超過10秒自動取消",
                            description="你想要刪除的項目是:"+str(self.label),
                            color=0x109319
                            )

        button1 = Button(label = "確認")
        async def button_callback(interaction):
            embed=discord.Embed(title="成功",
                                description=(str(self.label)+" 刪除成功"),
                                color=0x109319
                                )


            for i in range(len(list1)):

                for a in range(1,20):
                    try:
                        if str(list1[i])+str(output[list1[i]+str(a)]) == str(self.label):
                            del output[list1[i]+str(a)]
                    
                    except (KeyError) :
                        pass
                    except (IndexError):
                        pass

            with open('.\setting.json', mode = 'w',encoding="utf-8",newline='') as jf :
                json.dump(output,jf,indent=10,ensure_ascii=False)
            view.remove_item(button1)
            view.remove_item(button2)
            await interaction.response.edit_message(embed=embed , view=view)
        button1.callback = button_callback

        button2 = Button(label = "取消")
        async def button_callback(interaction):
            embed=discord.Embed(title="取消刪除",
                                description="取消成功!",
                                color=0x109319
                                )
            view.remove_item(button1)
            view.remove_item(button2)
            await interaction.response.edit_message(embed=embed , view=view)
        button2.callback = button_callback

        view = View()
        view.add_item(button1)
        view.add_item(button2)
        await interaction.response.send_message(embed=embed , view=view)
        try:
            interaction = await bot.wait_for("button_click", timeout=10)
        except asyncio.TimeoutError:
            try:
                embed=discord.Embed(title="取消刪除",
                                description="取消成功!",
                                color=0x109319
                                )
                view.remove_item(button1)
                view.remove_item(button2)
                await interaction.response.edit_message(embed=embed , view=view)
            except(discord.errors.InteractionResponded):
                return
        await interaction.response.defer()
        


@bot.command()
async def clean(ctx):
    await ctx.channel.purge()

    embed=discord.Embed(title="主頁",
                        description="這是一個目的為替代聯絡簿的機器人",
                        color=0x109319
                        )
    embed.set_author(name="吳瑞宸 盧宣嘉")

    if output["channelID"] == "" :
        embde.add_field(name="提醒",
                        value="記得要設定頻道ID!",
                        inline=False
                        )

    view = View()

    button1 = button_idget("idget")
    button2 = button_add_add("add",discord.ButtonStyle.green)
    button3 = button_pri_add("pri",discord.ButtonStyle.blurple)
    button4 = button_del_add("del",discord.ButtonStyle.red)

    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)
    view.add_item(button4)

    await ctx.send(embed=embed , view=view)

bot.run(output["TOKEN"])