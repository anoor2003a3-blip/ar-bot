import os
os.system("pip install yt-dlp python-telegram-bot")

import json
import random
import asyncio
from telegram import *
from telegram.ext import *

T = "8303634172:AAFAu8zC7RWFPRSOOXM_lYAflVKt489stKw"
D = 8217288002

def g():
    try:
        f = open("an.json","r")
        d = json.load(f)
        f.close()
        return d
    except:
        return {"r":{},"t":{},"s":{},"m":""}

def s(d):
    f = open("an.json","w")
    json.dump(d,f)
    f.close()

async def inf(u,c,i,db,w):
    try:
        t = await c.bot.get_chat(i)
        n = t.first_name
        un = f"@{t.username}" if t.username else "لا يوجد"
        v = db["s"].get(str(i),0)
        m = f"👤: {n}\n🆔: {i}\n🔗: {un}\n💬: {v}\n📌: {w}"
        try:
            p = await c.bot.get_user_profile_photos(i,limit=1)
            if p.total_count > 0:
                await u.message.reply_photo(p.photos[0][-1].file_id,caption=m)
            else: await u.message.reply_text(m)
        except: await u.message.reply_text(m)
    except: await u.message.reply_text("❌")

async def h(u,c):
    if not u.message or not u.message.text: return
    db = g()
    tx = u.message.text
    id = str(u.effective_user.id)
    db["s"][id] = db["s"].get(id,0) + 1
    s(db)

    if tx.startswith("يوت"):
        nm = tx.replace("يوت","").strip()
        if nm:
            await u.message.reply_text(f"⏳ جاري تحميل '{nm}'...")
            try:
                import yt_dlp
                f_n = f"s_{random.randint(1,999)}.mp3"
                opts = {'format':'bestaudio','outtmpl':f_n,'quiet':True}
                with yt_dlp.YoutubeDL(opts) as y:
                    y.download([f"ytsearch1:{nm}"])
                await u.message.reply_audio(audio=open(f_n,'rb'), title=nm)
                os.remove(f_n)
            except:
                await u.message.reply_text(f"❌ حاول مرة أخرى بعد دقيقة.")
            return

    if tx == "لو خيروك":
        ls = ["تاكل بصل أو تشرب خل؟", "تنام بقبر أو تعيش بغابة؟"]
        await u.message.reply_text(random.choice(ls))
        return

    if tx in ["اسالني", "اسألني"]:
        ls = ["شنو برجك؟", "شنو حلمك؟", "شنو أكثر شي تحبه؟"]
        await u.message.reply_text(random.choice(ls))
        return

    if tx == "ا":
        t = u.message.reply_to_message.from_user if u.message.reply_to_message else u.effective_user
        await inf(u,c,t.id,db,"كشف")
        return

    if tx in db["t"]: await inf(u,c,db["t"][tx],db,tx); return
    if tx in db["r"]: await u.message.reply_text(db["r"][tx])

app = Application.builder().token(T).build()
app.add_handler(MessageHandler(filters.TEXT,h))
print("🚀 STARTED")
app.run_polling()
