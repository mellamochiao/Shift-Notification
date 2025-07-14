import gspread
import requests
import discord
import asyncio
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import json

# ======== 設定區 ========
load_dotenv()
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")
TARGET_ROLE_NAME = os.getenv("TARGET_ROLE_NAME")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SHEET_NAME = os.getenv("SHEET_NAME")
SERVICE_ACCOUNT_INFO = json.loads(os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON"))
# =========================

# Google Sheets 認證
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(SERVICE_ACCOUNT_INFO, scope)
client = gspread.authorize(creds)

# 開啟 Google Sheet
spreadsheet = client.open_by_key(SPREADSHEET_ID)
sheet = spreadsheet.worksheet(SHEET_NAME)

# 取得明天日期
target_date = datetime.now() + timedelta(days=1)
date_str = target_date.strftime("%-m/%-d").replace("/0", "/")
all_values = sheet.get_all_values()

# 找出日期位置
target_row, target_col = None, None
for r_idx, row in enumerate(all_values):
    for c_idx, cell in enumerate(row):
        if cell.strip() == date_str:
            target_row = r_idx + 1
            target_col = c_idx + 1
            break
    if target_row:
        break

if not target_row:
    print(f"❌ 找不到日期 {date_str}")
    exit()

# 讀取排班人名（每格可能有多位 \n 分隔）
def get_shift_names(start_row, col):
    names = []
    for r in range(start_row, start_row + 7):
        val = sheet.cell(r, col).value
        if val and val.strip():
            split = [name.strip().replace(" ", "").replace("\u3000", "") for name in val.split("\n") if name.strip()]
            names.extend(split)
    return names

early_names = get_shift_names(target_row + 1, target_col)
night_names = get_shift_names(target_row + 9, target_col)

# ========== Discord 登入抓 ID ==========
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"🤖 Bot 登入成功：{client.user}")
    name_to_mention = {}

    for guild in client.guilds:
        async for member in guild.fetch_members(limit=None):
            for role in member.roles:
                if role.name == TARGET_ROLE_NAME:
                    clean_name = member.display_name.strip().replace(" ", "").replace("\u3000", "")
                    if clean_name in early_names + night_names:
                        name_to_mention[clean_name] = f"<@{member.id}>"

    # mention 
    def mentionize(names):
        mentions = []
        for name in names:
            if name in name_to_mention:
                mentions.append(name_to_mention[name])
            else:
                mentions.append(name)
        return mentions

    early_mentions = mentionize(early_names)
    night_mentions = mentionize(night_names)

    msg = f"""{date_str} 排班提醒 🐶
    
早班 11:00 開始  
{" ".join(early_mentions) or "（沒人）"}
    
晚班 18:00 開始  
{" ".join(night_mentions) or "（沒人）"}

提醒：排班完記得簽名喔
    """
    print("✅ 傳送內容如下：\n" + msg)
    requests.post(WEBHOOK_URL, json={"content": msg})
    await client.close()

# 執行 bot
asyncio.run(client.start(BOT_TOKEN))
