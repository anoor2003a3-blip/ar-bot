import telebot
import random

# الإعدادات
TOKEN = "8303634172:AAFAu8zC7RWFPRSOOXM_lYAflVKt489stKw"
bot = telebot.TeleBot(TOKEN)

# --- 1. الردود والتاكات (مؤقتة) ---
responses = {}
tags = {}

# --- 2. أمر الكشف (للجميع) ---
@bot.message_handler(func=lambda m: m.text == "كشف")
def kashf(message):
    user = message.from_user
    info = f"👤 اسمك: {user.first_name}\n🆔 أيديك: {user.id}\n🔗 يوزرك: @{user.username}"
    bot.reply_to(message, info)

# --- 3. الأوامر الخاصة (ردود وتاكات) ---
@bot.message_handler(func=lambda m: True)
def handle_msg(message):
    text = message.text
    # ملاحظة: لإضافة رد استخدم (اضف رد كلمة = جواب)
    if text.startswith("اضف رد"):
        try:
            parts = text.split("اضف رد ")[1].split("=")
            responses[parts[0].strip()] = parts[1].strip()
            bot.reply_to(message, "✅ تم إضافة الرد")
        except: pass

    elif text.startswith("اضف تاك"):
        try:
            parts = text.split("اضف تاك ")[1].split("=")
            tags[parts[0].strip()] = parts[1].strip()
            bot.reply_to(message, "✅ تم إضافة التاك")
        except: pass

    # تنفيذ الردود والتاكات
    elif text in responses:
        bot.reply_to(message, responses[text])
    elif text in tags:
        bot.send_message(message.chat.id, f"{tags[text]} @all")
    
    # أمر الحالة
    elif text == "بوت":
        bot.reply_to(message, "أوامر التحكم:\n- اضف رد [كلمة] = [رد]\n- اضف تاك [اسم] = [نص]")

# --- تشغيل البوت ---
if __name__ == "__main__":
    bot.remove_webhook() # تنظيف أي تعليق قديم
    print("البوت يعمل الآن بنجاح...")
    bot.infinity_polling()
