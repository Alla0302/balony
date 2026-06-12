"""
get_session.py — ЗАПУСТИ ОДИН РАЗ на компʼютері, щоб отримати TG_SESSION.
  1) pip install telethon
  2) python get_session.py  → введи api_id, api_hash, номер телефону, код із Telegram
  3) скопіюй надрукований рядок у GitHub → Settings → Secrets → TG_SESSION
"""
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = int(input("api_id: ").strip())
api_hash = input("api_hash: ").strip()
with TelegramClient(StringSession(), api_id, api_hash) as client:
    print("\n=== TG_SESSION (скопіюй цей рядок у GitHub Secret) ===\n")
    print(client.session.save())
    print()
