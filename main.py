import os
os.system("pip install yt-dlp python-telegram-bot")

import json, random, asyncio
from telegram import *
from telegram.ext import *

# إعدادات البوت
T = "8303634172:AAFAu8zC7RWFPRSOOXM_lYAflVKt489stKw"
OWNER_ID = 8217288002

def g():
    try:
        return json.load(open("an.json","r"))
    except:
        return {"r":{}, "t":{}, "s":{}, "m":""}

def s(d):
    json.dump(d, open("an.json","w"))

async def h(u, c):
    if not u.message or not u.message.text: return
    db = g()
    tx = u.message.text
    id = str(u.effective_user.id)
    
    # حفظ الإحصائيات
    db["s"][id] = db["s"].get(id, 0) + 1
    s(db)

    # ميزة الهمسة (بالرد)
    if tx.startswith("همسه") or tx.startswith("همسة"):
        if u.message.reply_to_message:
            to_user = u.message.reply_to_message.from_user
            msg = tx.replace("همسه","").replace("همسة","").strip()
            k = InlineKeyboardMarkup([[InlineKeyboardButton(f"الهمسة لـ {to_user.first_name}", callback_data=f"h_{to_user.id}")]])
            db["m"] = msg
            s(db)
            await u.message.reply_text("✅ تم إرسال الهمسة بنجاح.", reply_markup=k)
        return

    # ميزة يوت (التحميل)
    if tx.startswith("يوت"):
        nm = tx.replace("يوت","").strip()
        if nm:
            m = await u.message.reply_text(f"⏳ جاري تحميل: {nm}...")
            try:
                import yt_dlp
                fn = f"{random.randint(1,999)}.mp3"
                with yt_dlp.YoutubeDL({'format':'bestaudio','outtmpl':fn,'quiet':True}) as y:
                    y.download([f"ytsearch1:{nm}"])
                await u.message.reply_audio(audio=open(fn,'rb'), title=nm)
                os.remove(fn)
                await m.delete()
            except:
                await m.edit_text("❌ فشل التحميل، جرب لاحقاً.")
        return

    # أوامر التحكم (لك فقط)
    if tx == "البوت" and u.effective_user.id == OWNER_ID:
        k = InlineKeyboardMarkup([
            [InlineKeyboardButton("+ رد", callback_data="add_r"), InlineKeyboardButton("- رد", callback_data="del_r")],
            [InlineKeyboardButton("+ تاك", callback_data="add_t"), InlineKeyboardButton("- تاك", callback_data="del_t")]
        ])
        await u.message.reply_text("🛠 أهلاً بك أنور.. تحكم بالبوت من هنا:", reply_markup=k)
        return

    # الردود التفاعلية
    if tx == "لو خيروك":
        await u.message.reply_text(random.choice(["تاكل بصل؟", "تشرب خل؟", "تنام بغابة؟"]))
    elif tx in ["اسألني", "اسالني"]:
        await u.message.reply_text(random.choice(["شنو برجك؟", "شنو حلمك؟", "منو قدوتك؟"]))
    elif tx in db["r"]:
        await u.message.reply_text(db["r"][tx])

# معالجة الضغط على الأزرار
async def cb(u, c):
    q = u.callback_query
    db = g()
    if q.data.startswith("h_"):
        uid = q.data.split("_")[1]
        if str(q.from_user.id) == uid:
            await q.answer(db.get("m", "لا توجد رسالة"), show_alert=True)
        else:
            await q.answer("الهمسة ليست لك! ❌", show_alert=True)

app = Application.builder().token(T).build()
app.add_handler(MessageHandler(filters.TEXT, h))
app.add_handler(CallbackQueryHandler(cb))
app.run_polling()
