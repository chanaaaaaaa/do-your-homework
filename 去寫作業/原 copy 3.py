import discord 
from discord.ext import commands
from discord.ui import Button, View
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
class ScheduleView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # 移除超時
        self.embed = discord.Embed(title="行程管理", color=0x109319)
        self.pr_button = discord.ui.Button(style=discord.ButtonStyle.secondary, label="行程清單", custom_id="pr")
        self.add_button = discord.ui.Button(style=discord.ButtonStyle.secondary, label="新增行程", custom_id="add")
        self.delete_button = discord.ui.Button(style=discord.ButtonStyle.secondary, label="刪除行程", custom_id="delete")
        self.add_item(self.pr_button)
        self.add_item(self.add_button)
        self.add_item(self.delete_button)
#"科目":"科目為 國文or英文or數學or物理or化學or生物or地科or地理or歷史or公民or美術or國防or新莊or生命
@bot.event
async def on_ready():
    now = datetime.datetime.now()
    print(now)

    check_expired_items3.start()
    print("機器啟動")
    bot.add_view(ScheduleView())



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
async def pr(ctx):
    view = ScheduleView()
    view.ctx = ctx
    view.message = await ctx.send(embed=view.embed, view=view)

@bot.command()
async def add(ctx):
    view = ScheduleView()
    view.ctx = ctx
    view.message = await ctx.send(embed=view.embed, view=view)

@bot.command()
async def delete(ctx):
    view = ScheduleView()
    view.ctx = ctx
    view.message = await ctx.send(embed=view.embed, view=view)

@bot.event
async def on_button_click(interaction: discord.Interaction):
    if interaction.component.custom_id == "pr":
        await pr_interaction(interaction)
    elif interaction.component.custom_id == "add":
        await add_interaction(interaction)
    elif interaction.component.custom_id == "delete":
        await delete_interaction(interaction)

async def pr_interaction(interaction: discord.Interaction):
    # 實現行程清單功能
    list1 = ["國文", "英文", "數學", "物理", "化學", "生物", "地科", "地理", "歷史", "公民", "美術", "國防", "新莊", "生命"]
    list2 = ["", "", "", "", "", "", "", "", "", "", "", "", "", ""]
    with open('.\setting.json', mode='r', encoding="utf-8", newline='') as jf:
        output = json.load(jf)

        if output["channelID"] == "":
            embed = discord.Embed(title="提醒", description="記得要設定頻道ID!", color=0xFF5733)
            await interaction.channel.send(embed=embed)

    embed = discord.Embed(title="全部行程", description="科目 - 時間 - 內容 - 編號", color=0x109319)

    for i in range(0, len(list1) - 1):
        try:
            for a in range(1, 21):
                if output[f'{list1[i]}{a}'] != "":
                    list2[i] += f'{list1[i]} - {output[f"{list1[i]}{a}"]} - {output[f"{list1[i]}{a}text"]} - {a}\n'
        except:
            pass

    for i in range(0, len(list1) - 1):
        embed.add_field(name=f'{list1[i]}', value=list2[i], inline=False)

    await interaction.message.edit(embed=embed)

async def add_interaction(interaction: discord.Interaction):
    # 實現新增行程功能
    await interaction.response.send_message("請選擇科目：", view=ScheduleView())

async def delete_interaction(interaction: discord.Interaction):
    # 實現刪除行程功能
    list1 = ["國文", "英文", "數學", "物理", "化學", "生物", "地科", "地理", "歷史", "公民", "美術", "國防", "新莊", "生命"]
    list2 = ["", "", "", "", "", "", "", "", "", "", "", "", "", ""]
    with open('.\setting.json', mode='r', encoding="utf-8", newline='') as jf:
        output = json.load(jf)

        if output["channelID"] == "":
            embed = discord.Embed(title="提醒", description="記得要設定頻道ID!", color=0xFF5733)
            await interaction.channel.send(embed=embed)

    for i in range(0, len(list1) - 1):
        try:
            for a in range(1, 21):
                if output[f'{list1[i]}{a}'] != "":
                    list2[i] += f'{list1[i]} - {output[f"{list1[i]}{a}"]} - {output[f"{list1[i]}{a}text"]} - {a}\n'
        except:
            pass

    embed = discord.Embed(title="刪除行程", description="科目 - 時間 - 內容 - 編號", color=0x109319)

    for i in range(0, len(list1) - 1):
        embed.add_field(name=f'{list1[i]}', value=list2[i], inline=False)

    await interaction.message.edit(embed=embed)




bot.run(output["TOKEN"])