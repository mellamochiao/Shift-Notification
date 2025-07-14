import discord
import csv
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# 啟用 intents
intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

# 身份組名稱
TARGET_ROLE_NAME = "暑假排班" 

@client.event
async def on_ready():
    print(f'Bot 已登入：{client.user}')

    for guild in client.guilds:
        print(f"\n 伺服器：{guild.name}")
        print("=" * 40)

        members_with_role = []

        # 確保 member 完整載入
        async for member in guild.fetch_members(limit=None):
            # 找出有目標身分組的成員
            for role in member.roles:
                if role.name == TARGET_ROLE_NAME:
                    members_with_role.append({
                        "name": member.display_name,
                        "discord_id": member.id,
                        "mention": f"<@{member.id}>"
                    })
                    break

        # 寫入 CSV 檔
        with open("member_id.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["name", "discord_id", "mention"])
            writer.writeheader()
            writer.writerows(members_with_role)

        print(f"共寫入 {len(members_with_role)} 位成員到 member_id.csv")

    await client.close()

client.run(BOT_TOKEN)