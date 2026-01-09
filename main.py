import telebot
from telebot import types
import random

# --- الإعدادات ---
TOKEN = "8303634172:AAFAu8zC7RWFPRSOOXM_lYAflVKt489stKw"
ADMIN_ID = 8217288002
bot = telebot.TeleBot(TOKEN)

# مخازن البيانات
responses = {}
tags = {}

# --- 1. أوامر الإدارة (أزرار شفافة + إحصائيات) ---
@bot.message_handler(func=lambda m: m.text == "بوت" and m.from_user.id == ADMIN_ID)
def admin_panel(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(f"الردود ({len(responses)})", callback_data="stats_res")
    btn2 = types.InlineKeyboardButton(f"التاكات ({len(tags)})", callback_data="stats_tags")
    btn3 = types.InlineKeyboardButton("➕ إضافة رد", callback_data="add_res")
    btn4 = types.InlineKeyboardButton("🗑️ حذف رد", callback_data="del_res")
    btn5 = types.InlineKeyboardButton("➕ إضافة تاك", callback_data="add_tag")
    btn6 = types.InlineKeyboardButton("🗑️ حذف تاك", callback_data="del_tag")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    
    bot.reply_to(message, "🛠️ **أهلاً بك في لوحة تحكم المطور**\nإليك الإحصائيات والأدوات:", reply_markup=markup, parse_mode="Markdown")

# --- 2. نظام الهمسة السرية (أزرار شفافة) ---
@bot.message_handler(func=lambda m: m.text.startswith("همسه"))
def create_whisper(message):
    try:
        parts = message.text.split(maxsplit=2)
        target_user = parts[1].replace("@", "")
        msg_content = parts[2]
        
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(f"اضغط لرؤية الهمسة 🤫", callback_data=f"show_{target_user}_{message.from_user.id}")
        markup.add(btn)
        
        # تخزين مؤقت للهمسة (في الذاكرة)
        if not hasattr(bot, 'whispers'): bot.whispers = {}
        whisper_id = f"{target_user}_{message.from_user.id}"
        bot.whispers[whisper_id] = msg_content
        
        bot.send_message(message.chat.id, f"👤 إرسال همسة إلى: @{target_user}\n🔐 لا يراها غيره!", reply_markup=markup)
        
        # إشعار للمطور
        bot.send_message(ADMIN_ID, f"🕵️‍♂️ **رقابة:**\nمن: @{message.from_user.username}\nإلى: @{target_user}\nالنص: {msg_content}")
    except:
        bot.reply_to(message, "⚠️ الطريقة: همسه @يوزر الكلام")

# --- 3. معالجة الأزرار (Callback Query) ---
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data.startswith("show_"):
        data = call.data.split("_")
        target = data[1]
        sender_id = int(data[2])
        whisper_id = f"{target}_{sender_id}"
        
        # التحقق: هل الضاغط هو المستلم أو المرسل أو المطور؟
        if call.from_user.username == target or call.from_user.id == sender_id or call.from_user.id == ADMIN_ID:
            msg = bot.whispers.get(whisper_id, "الهمسة منتهية الصلاحية!")
            bot.answer_callback_query(call.id, f"الرسالة: {msg}", show_alert=True)
        else:
            bot.answer_callback_query(call.id, "❌ هذه الهمسة ليست لك!", show_alert=True)
            
    elif call.data == "stats_res":
        bot.answer_callback_query(call.id, f"عدد الردود المضافة: {len(responses)}", show_alert=True)
    elif call.data == "stats_tags":
        bot.answer_callback_query(call.id, f"عدد التاكات المضافة: {len(tags)}", show_alert=True)
    elif call.data in ["add_res", "del_res", "add_tag", "del_tag"]:
        bot.answer_callback_query(call.id, "استخدم الأوامر النصية حالياً (اضف رد كلمة = جواب)", show_alert=True)

# --- 4. أمر الكشف (حرف ا) ---
@bot.message_handler(func=lambda m: m.text == "ا")
def kashf(message):
    user = message.from_user
    status = random.choice(["متفاعل نار 🔥", "صنم 🗿", "متفاعل متوسط ✨"])
    info = f"👤 **الاسم:** {user.first_name}\n🆔 **الأيدي:** `{user.id}`\n📈 **التفاعل:** {status}"
    photos = bot.get_user_profile_photos(user.id)
    if photos.total_count > 0:
        bot.send_photo(message.chat.id, photos.photos[0][-1].file_id, caption=info, parse_mode="Markdown")
    else: bot.reply_to(message, info, parse_mode="Markdown")

# --- 5. تشغيل البوت ---
@bot.message_handler(func=lambda m: True)
def text_handler(message):
    # معالجة إضافة الردود والتاكات نصياً لسهولة الاستخدام
    if message.from_user.id == ADMIN_ID:
        if "اضف رد" in message.text:
            p = message.text.split("اضف رد ")[1].split("=")
            responses[p[0].strip()] = p[1].strip()
            bot.reply_to(message, "✅ تم إضافة الرد")
        elif "اضف تاك" in message.text:
            p = message.text.split("اضف تاك ")[1].split("=")
            tags[p[0].strip()] = p[1].strip()
            bot.reply_to(message, "✅ تم إضافة التاك")
    
    if message.text in responses: bot.reply_to(message, responses[message.text])

if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling()
