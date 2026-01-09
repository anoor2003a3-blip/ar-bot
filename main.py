import telebot
from telebot import types
import random

# --- الإعدادات ---
TOKEN = "8303634172:AAFAu8zC7RWFPRSOOXM_lYAflVKt489stKw"
ADMIN_ID = 8217288002
bot = telebot.TeleBot(TOKEN)

# مخازن البيانات (ستحتاج لقاعدة بيانات لحفظها دائماً، حالياً هي بالذاكرة)
responses = {}
user_msg_count = {} # لحساب عدد الرسائل

# --- قائمة الأسئلة والخيارات ---
questions = ["هل أنت شخص متسامح؟", "ما هو أكبر مخاوفك؟", "من هو قدوتك؟", "أكثر شيء ندمت عليه؟"] + [f"سؤال {i}: ما هو هدفك القادم؟" for i in range(5, 105)]
choices = ["تاكل صرصور 🪳 أو تشرب خـل 🥃؟", "تخسر فونك 📱 أو تعيش بدون نت 🌐؟", "تكون بطل خارق 🦸‍♂️ أو ملياردير 💰؟"]

# --- 1. حساب الرسائل (تحديث تلقائي) ---
@bot.message_handler(func=lambda m: True, content_types=['text'])
def monitor_messages(message):
    uid = message.from_user.id
    user_msg_count[uid] = user_msg_count.get(uid, 0) + 1
    
    # تنفيذ الأوامر داخل هذا المعالج لضمان عملها
    text = message.text
    
    if text == "ا":
        kashf_logic(message)
    elif text == "بوت" and uid == ADMIN_ID:
        admin_panel(message)
    elif text.startswith("همسه"):
        create_whisper(message)
    elif text == "اسألني":
        bot.reply_to(message, random.choice(questions))
    elif text == "لو خيروك":
        bot.reply_to(message, random.choice(choices))
    elif message.reply_to_message and text == "تاك":
        tag_logic(message)
    elif text in responses:
        bot.reply_to(message, responses[text])
    elif text.startswith("اضف رد") and uid == ADMIN_ID:
        try:
            p = text.split("اضف رد ")[1].split("=")
            responses[p[0].strip()] = p[1].strip()
            bot.reply_to(message, "✅ تم إضافة الرد")
        except: pass

# --- 2. منطق الكشف (حرف ا) ---
def kashf_logic(message):
    user = message.from_user
    msg_count = user_msg_count.get(user.id, 1)
    status = "نار 🔥" if msg_count > 50 else "متفاعل ✨"
    info = f"👤 **الاسم:** {user.first_name}\n🆔 **الأيدي:** `{user.id}`\n📧 **يوزر:** @{user.username}\n📊 **رسائلك:** {msg_count}\n📈 **تفاعلك:** {status}"
    photos = bot.get_user_profile_photos(user.id)
    if photos.total_count > 0:
        bot.send_photo(message.chat.id, photos.photos[0][-1].file_id, caption=info, parse_mode="Markdown")
    else: bot.reply_to(message, info, parse_mode="Markdown")

# --- 3. التاك المطور (مثل الكشف) ---
def tag_logic(message):
    target = message.reply_to_message.from_user
    count = user_msg_count.get(target.id, "غير محسوب")
    info = f"🎯 **تم عمل تاك للمستخدم:**\n\n👤 **الاسم:** {target.first_name}\n🆔 **الأيدي:** `{target.id}`\n📧 **يوزر:** @{target.username}\n💬 **عدد رسائله:** {count}\n📢 **بواسطة:** @{message.from_user.username}"
    bot.reply_to(message, info, parse_mode="Markdown")

# --- 4. لوحة التحكم (أزرار) ---
def admin_panel(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(f"الردود ({len(responses)})", callback_data="none")
    btn2 = types.InlineKeyboardButton("➕ إضافة رد", callback_data="instruct")
    markup.add(btn1, btn2)
    bot.reply_to(message, "🛠️ لوحة التحكم:", reply_markup=markup)

# --- 5. الهمسة السرية ---
def create_whisper(message):
    try:
        parts = message.text.split(maxsplit=2)
        target_user = parts[1].replace("@", "")
        msg = parts[2]
        if not hasattr(bot, 'whispers'): bot.whispers = {}
        bot.whispers[f"{target_user}_{message.from_user.id}"] = msg
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("كشف الهمسة 🔐", callback_data=f"show_{target_user}_{message.from_user.id}"))
        bot.send_message(message.chat.id, f"👤 همسة لـ @{target_user}\nمن @{message.from_user.username}", reply_markup=markup)
        bot.send_message(ADMIN_ID, f"🕵️ الرقيب:\nمن: @{message.from_user.username}\nإلى: @{target_user}\nالنص: {msg}")
    except: bot.reply_to(message, "⚠️ همسه @يوزر النص")

# --- معالجة الأزرار ---
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data.startswith("show_"):
        data = call.data.split("_")
        if call.from_user.username == data[1] or call.from_user.id == int(data[2]) or call.from_user.id == ADMIN_ID:
            msg = bot.whispers.get(f"{data[1]}_{data[2]}", "خطأ!")
            bot.answer_callback_query(call.id, f"الهمسة: {msg}", show_alert=True)
        else: bot.answer_callback_query(call.id, "❌ ليست لك!", show_alert=True)
    elif call.data == "instruct":
        bot.answer_callback_query(call.id, "اكتب: اضف رد كلمة = جواب", show_alert=True)

if __name__ == "__main__":
    bot.infinity_polling()
