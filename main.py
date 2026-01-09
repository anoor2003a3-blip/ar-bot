import telebot
import os
import random
import yt_dlp

# ضع توكن بوتك هنا
TOKEN = "7929849202:AAH9f73mX1vYx33p-2z7mG_uR33p-z3m"
bot = telebot.TeleBot(TOKEN)

# --- 1. أوامر البداية والكشف ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "أهلاً بك في البوت العملاق! 🤖\nأنا أعمل الآن بكامل طاقتي.")

@bot.message_handler(func=lambda m: m.text == "البوت")
def bot_status(message):
    bot.reply_to(message, "أنا شغال وعال العال! ✅")

@bot.message_handler(func=lambda m: m.text == "كشف")
def kashf(message):
    user = message.from_user
    info = f"👤 اسمك: {user.first_name}\n🆔 أيديك: {user.id}\n username: @{user.username}"
    bot.reply_to(message, info)

# --- 2. الألعاب (اسألني ولو خيروك) ---
questions = ["هل أنت صريح؟", "ما هو حلمك؟", "من هو قدوتك؟"]
choices = ["تاكل ليمون 🍋 أو فلفل 🌶️؟", "تنام بالشارع ⛺ أو بكهف 🦇؟"]

@bot.message_handler(func=lambda m: m.text == "اسألني")
def ask_me(message):
    bot.reply_to(message, random.choice(questions))

@bot.message_handler(func=lambda m: m.text == "لو خيروك")
def choose_me(message):
    bot.reply_to(message, random.choice(choices))

# --- 3. التاكات (للجروبات) ---
@bot.message_handler(func=lambda m: m.text == "تاك")
def tag_all(message):
    bot.send_message(message.chat.id, "نداء للجميع! 📣 @all")

# --- 4. الهمسة (سرية) ---
@bot.message_handler(commands=['whisper'])
def whisper(message):
    bot.reply_to(message, "أرسل همستك بهذا الشكل: /whisper [اليوزر] [الرسالة]")

# --- 5. تحميل اليوتيوب (يوت) ---
@bot.message_handler(commands=['ytdl'])
def download_yt(message):
    url = message.text.split()[1] if len(message.text.split()) > 1 else None
    if url:
        bot.reply_to(message, "جاري معالجة الرابط... ⏳")
        # ملاحظة: يتطلب وجود مكتبة yt-dlp
    else:
        bot.reply_to(message, "أرسل الرابط بعد الأمر")

# --- تشغيل البوت مع خدعة المنفذ لـ Koyeb ---
if __name__ == "__main__":
    print("البوت العملاق بدأ العمل...")
    # تشغيل البوت للأبد
    bot.infinity_polling()
