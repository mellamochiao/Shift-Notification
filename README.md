# Shift Notification Discord Bot🐶

A scheduled Discord bot to automatically remind volunteer shifts from Google Sheets.

##  Project Description

This project automates the process of sending daily shift reminders to a Discord channel. It is designed for volunteer teams that maintain a shared schedule on Google Sheets. The script reads tomorrow’s shift names from the spreadsheet, converts them into Discord mentions using role filtering, and sends a formatted message to a designated channel using Discord Webhook.
The project is now deployed on [Render.com](https://render.com), where a cron job is scheduled to run once per day.

##  Features

- Automatically fetches tomorrow’s date and shift info from Google Sheets.
- Converts names into actual Discord user mentions using role-based matching.
- Sends shift reminder to a specified Discord channel.
- Runs daily via cron job on Render.com.

## Technologies Used

- Python 3
- [gspread](https://github.com/burnash/gspread) – access Google Sheets API
- [discord.py](https://discordpy.readthedocs.io/) – fetch guild member info
- Discord Webhook API – post messages
- Render.com – cloud deployment (cron job)

## 🗂️ Files in This Repository

| File              | Description                                                        |
|-------------------|--------------------------------------------------------------------|
| `main.py`         | Main script to fetch shift info from Google Sheets and send reminders via Discord Webhook |
| `member_id.py`    | Utility script to fetch all members with a specific role and export their names and Discord IDs to `member_id.csv` |
| `requirements.txt`| Python dependencies required to run the project                   |


## API Keys & Secrets

Sensitive credentials (such as Webhook URL, bot token, spreadsheet ID, and service account JSON) are **not** included in the repository. They are managed via environment variables:

```env
WEBHOOK_URL="..."
BOT_TOKEN="..."
TARGET_ROLE_NAME="..."
SPREADSHEET_ID="..."
SHEET_NAME="..."
GOOGLE_SERVICE_ACCOUNT_JSON="..."  # Entire content of service_account.json 
```
⚠️ GOOGLE_SERVICE_ACCOUNT_JSON is stored as a string in the .env file, and dynamically written to a temp file at runtime.

## Author
[mellamochiao](https://github.com/mellamochiao)
