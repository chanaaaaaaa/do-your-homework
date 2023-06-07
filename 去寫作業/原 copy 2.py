import discord
from discord.ext import commands
from discord.ui import Button, View
import asyncio
import datetime
from discord.ext import tasks
import json
import time
import asyncio
from datetime import timedelta
import os
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='=', intents=intents)

with open('./setting.json', mode='r', encoding="utf8", newline='') as jf:
    output = json.load(jf)

list1 = ["國文", "英文", "數學", "物理", "化學", "生物", "地科", "地理", "歷史", "公民", "美術", "國防", "新莊", "生命"]

@bot.event
async def on_ready():
    now = datetime.datetime.now()
    print(now)

    check_expired_items3.start()
    
    # 創建 ScheduleView 的實例
    schedule_view = ScheduleView()

    # 將 ScheduleView 的實例添加為一個互動事件監聽器
    bot.add_view(schedule_view)
    join_button = Button(label="加入", style=discord.ButtonStyle.primary)
    delete_button = Button(label="刪除", style=discord.ButtonStyle.danger)
    browse_button = Button(label="瀏覽", style=discord.ButtonStyle.secondary)

    # 添加預設按鈕到視圖
    schedule_view.clear_items()
    schedule_view.add_item(join_button)
    schedule_view.add_item(delete_button)
    schedule_view.add_item(browse_button)

    # 在你想要顯示日程安排的頻道中創建視圖消息
    channel = bot.get_channel(output["channelID"])  # 將 "頻道ID" 替換為實際的頻道ID
    await channel.send(embed=discord.Embed(title="日程安排", description="點擊下面的按鈕來操作日程安排"), view=schedule_view)
    

@tasks.loop(minutes=60)
async def check_expired_items3():
    list1 = ["國文", "英文", "數學", "物理", "化學", "生物", "地科", "地理", "歷史", "公民", "美術", "國防", "新莊", "生命"]
    now = datetime.datetime.now()

    for a in range(0, len(list1) - 1):
        try:
            for i in range(1, 20):
                item = output.get(str(list1[a]) + str(i))
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
                    del output[str(list1[a]) + str(i)]
                    with open("setting.json", "w", encoding="utf8") as jf:
                        json.dump(output, jf, ensure_ascii=False)
                    print(f"項目 {list1[a]}{i} 已過期，已自動刪除")

                    embed = discord.Embed(title="刪除",
                                          description=f"項目 {list1[a]} 編號{i} 已過期，已自動刪除",
                                          color=0xFF5733)
                    await bot.get_channel(output["channelID"]).send(embed=embed)

        except Exception as e:
            print(f"處理項目 {list1[a]} 時發生錯誤：{e}")

    await asyncio.sleep(10)


@bot.command()
async def idget(ctx):
    embed = discord.Embed(title="成功",
                          description="取得成功",
                          color=0x109319)
    await ctx.send(embed=embed)
    output["channelID"] = ctx.channel.id

    with open('./setting.json', mode='w', encoding="utf-8", newline='') as jf:
        json.dump(output, jf, indent=10, ensure_ascii=False)


@bot.command()
async def hi(ctx):

    if output["channelID"] == "":
        embed = discord.Embed(title="提醒",
                              description="記得要設定頻道ID!",
                              color=0xFF5733)
        await ctx.send(embed=embed)

    embed = discord.Embed(title="成功",
                          description="測試成功",
                          color=0xFF5733)
    await ctx.send(embed=embed)


class ScheduleView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.clear_items()

    def clear_items(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    async def on_button_click(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.send(f"You clicked the {button.label} button!")

        if button.custom_id.startswith("delete_button"):
            await self.delete_schedule(interaction, button.custom_id)

    async def display_schedule_list(self, interaction):
        embed = discord.Embed(title="全部行程", description="科目 - 時間 - 內容 - 編號", color=0x109319)

        for i in range(0, len(list1) - 1):
            for j in range(1, 20):
                item = output.get(f"{list1[i]}{j}")
                if item:
                    time_str = item[0]
                    subject = item[1]
                    content = item[2]
                    num = j

                    embed.add_field(name=f"{subject} - {time_str} - {content} - 編號 {num}", value="\u200b", inline=False)

        await interaction.send(embed=embed, ephemeral=True)

    async def delete_schedule(self, interaction, custom_id):
        def check_author(m):
            return m.author == interaction.user and m.channel == interaction.channel

        schedule_id = custom_id.split("_")[-1]  # Extract the schedule ID from the custom ID
        subject, num = schedule_id[:-1], int(schedule_id[-1])

        item_key = f"{subject}{num}"
        item = output.get(item_key)

        if item:
            del output[item_key]
            with open("setting.json", "w", encoding="utf8") as jf:
                json.dump(output, jf, ensure_ascii=False)
            print(f"項目 {item_key} 已過期，已自動刪除")

            embed = discord.Embed(
                title="刪除",
                description=f"項目 {item_key} 已過期，已自動刪除",
                color=0xFF5733
            )
            await bot.get_channel(output["channelID"]).send(embed=embed)

            await interaction.send(f"已刪除行程：{item_key}", ephemeral=True)
        else:
            await interaction.send("無效的行程編號！", ephemeral=True)


@bot.command()
async def showschedule(ctx):
    schedule_view = ScheduleView()
    # 创建默认按钮
    join_button = Button(label="加入", style=discord.ButtonStyle.primary)
    delete_button = Button(label="刪除", style=discord.ButtonStyle.danger)
    browse_button = Button(label="瀏覽", style=discord.ButtonStyle.secondary)

    # 添加默认按钮到视图
    schedule_view.clear_items()
    schedule_view.add_item(join_button)
    schedule_view.add_item(delete_button)
    schedule_view.add_item(browse_button)

    # 在此命令中调用 display_schedule_list 方法显示日程安排列表
    await schedule_view.display_schedule_list(ctx)


bot.run(output["TOKEN"])