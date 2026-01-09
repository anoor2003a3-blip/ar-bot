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
user_msg_count = {}

# قوائم الأسئلة
questions = ["هل أنت شخص متسامح؟", "ما هو أكبر مخاوفك؟", "من هو قدوتك؟"] + [f"سؤال {i}: ما هو هدفك القادم؟" for i in range(4, 101)]
choices = ["تاكل فلفل حار 🌶️ أو ليمون حامض 🍋؟", "تخسر فونك 📱 أو تعيش بدون نت 🌐؟"]

# --- 1. حساب الرسائل ---
@bot.message_handler(func=lambda m: True, content_types=['text'])
def main_handler(message):
    uid = message.from_user.id
    user_msg_count[uid] = user_msg_count.get(uid, 0) + 1
    text = message.text

    # أوامر مباشرة
    if text == "ا": kashf_logic(message)
    elif text == "بوت" and uid == ADMIN_ID: admin_panel(message)
    elif text.startswith("همسه"): create_whisper(message)
    elif text == "اسألني": bot.reply_to(message, random.choice(questions))
    elif text == "لو خيروك": bot.reply_to(message, random.choice(choices))
    elif message.reply_to_message and text == "تاك": tag_logic(message)
    
    # تنفيذ الردود والتاكات المضافة
    elif text in responses: bot.reply_to(message, responses[text])
    elif text in tags: bot.send_message(message.chat.id, f"{tags[text]} @all")
    
    # معالجة الإضافة والحذف نصياً (للمطور)
    if uid == ADMIN_ID:
        if text.startswith("اضف رد"):
            try:
                p = text.split("اضف رد ")[1].split("=")
                responses[p[0].strip()] = p[1].strip()
                bot.reply_to(message, "✅ تم إضافة الرد")
            except: pass
        elif text.startswith("حذف رد"):
            word = text.split("حذف رد ")[1].strip()
            responses.pop(word, None)
            bot.reply_to(message, "🗑️ تم حذف الرد")
        elif text.startswith("اضف تاك"):
            try:
                p = text.split("اضف تاك ")[1].split("=")
                tags[p[0].strip()] = p[1].strip()
                bot.reply_to(message, "✅ تم إضافة التاك")
            except: pass
        elif text.startswith("حذف تاك"):
            word = text.split("حذف تاك ")[1].strip()
            tags.pop(word, None)
            bot.reply_to(message, "🗑️ تم حذف التاك")

# --- 2. لوحة التحكم (أزرار شفافة) ---
def admin_panel(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(f"الردود ({len(responses)})", callback_data="none")
    btn2 = types.InlineKeyboardButton(f"التاكات ({len(tags)})", callback_data="none")
    btn3 = types.InlineKeyboardButton("➕ إضافة رد", callback_data="instr")
    btn4 = types.InlineKeyboardButton("🗑️ حذف رد", callback_data="instr")
    btn5 = types.InlineKeyboardButton("➕ إضافة تاك", callback_data="instr")
    btn6 = types.InlineKeyboardButton("🗑️ حذف تاك", callback_data="instr")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    bot.reply_to(message, "🛠️ **لوحة التحكم والإحصائيات:**", reply_markup=markup, parse_mode="Markdown")

# --- 3. التاك المطور (مثل الكشف) ---
def tag_logic(message):
    target = message.reply_to_message.from_user
    count = user_msg_count.get(target.id, 0)
    info = f"🎯 **تـم عـمل تـاك لـلـعـضـو:**\n\n"
    info += f"👤 **الاسم:** {target.first_name}\n"
    info += f"🆔 **الأيدي:** `{target.id}`\n"
    info += f"📧 **يوزر:** @{target.username if target.username else 'لا يوجد'}\n"
    info += f"💬 **رسائله:** {count}\n"
    info += f"📢 **بواسطة:** {message.from_user.first_name}"
    
    photos = bot.get_user_profile_photos(target.id)
    if photos.total_count > 0:
        bot.send_photo(message.chat.id, photos.photos[0][-1].file_id, caption=info, parse_mode="Markdown")
    else: bot.reply_to(message, info, parse_mode="Markdown")

# --- 4. منطق الكشف (حرف ا) ---
def kashf_logic(message):
    user = message.from_user
    count = user_msg_count.get(user.id, 0)
    info = f"👤 **معلوماتك:**\n🆔 **الأيدي:** `{user.id}`\n📊 **الرسائل:** {count}"
    photos = bot.get_user_profile_photos(user.id)
    if photos.total_count > 0:
        bot.send_photo(message.chat.id, photos.photos[0][-1].file_id, caption=info, parse_mode="Markdown")
    else: bot.reply_to(message, info, parse_mode="Markdown")

# --- 5. الهمسة السرية ---
def create_whisper(message):
    try:
        parts = message.text.split(maxsplit=2)
        target = parts[1].replace("@", "")
        if not hasattr(bot, 'whispers'): bot.whispers = {}
        bot.whispers[f"{target}_{message.from_user.id}"] = parts[2]
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("كشف الهمسة 🔐", callback_data=f"sw_{target}_{message.from_user.id}"))
        bot.send_message(message.chat.id, f"👤 إرسال همسة إلى: @{target}\n🔐 لا يراها غيره!", reply_markup=markup)
        bot.send_message(ADMIN_ID, f"🕵️ رقابة: من @{message.from_user.username} إلى @{target}\nالنص: {parts[2]}")
    except: bot.reply_to(message, "⚠️ همسه @يوزر النص")

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data.startswith("sw_"):
        d = call.data.split("_")
        if call.from_user.username == d[1] or call.from_user.id == int(d[2]) or call.from_user.id == ADMIN_ID:
            bot.answer_callback_query(call.id, f"الهمسة: {bot.whispers.get(f'{d[1]}_{d[2]}')}", show_alert=True)
        else: bot.answer_callback_query(call.id, "❌ ليست لك!", show_alert=True)
    elif call.data == "instr":
        bot.answer_callback_query(call.id, "استخدم الأوامر: (اضف رد / حذف رد / اضف تاك / حذف تاك)", show_alert=True)

if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling()
