from pyrogram import Client, filters
import requests
import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("tiktok_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def download_tiktok(url):
    try:
        clean_url = url.split("?")[0]
        api_url = f"https://tikwm.com/api/?url={clean_url}"
        response = requests.get(api_url).json()
        if response["data"]:
            return response["data"]["play"], response["data"]["title"]
        else:
            return None, "فشل في الحصول على الفيديو"
    except Exception as e:
        return None, str(e)

@app.on_message(filters.private & filters.text)
def handle_message(client, message):
    text = message.text
    if "tiktok.com" in text:
        msg = message.reply("⏳ جاري التحميل بدون علامة مائية ...")
        video_url, title = download_tiktok(text)

        if video_url:
            msg.edit("📤 جاري إرسال الفيديو ...")
            client.send_video(message.chat.id, video=video_url, caption=title)
        else:
            msg.edit(f"❌ حدث خطأ: {title}")
    else:
        message.reply("📌 أرسل رابط فيديو من تيك توك فقط.")

app.run()
