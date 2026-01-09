import telebot
import os
import random
import yt_dlp

# الإعدادات الأساسية
TOKEN = "8303634172:AAFAu8zC7RWFPRSOOXM_lYAflVKt489stKw"
DEVELOPER_ID = 123456789  # !!! ضع أيديك هنا لكي تصلك الهمسات !!!
bot = telebot.TeleBot(TOKEN)

# --- 1. أوامر الحالة والكشف ---
@bot.message_handler(func=lambda m: m.text == "البوت")
def bot_status(message):
    bot.reply_to(message, "أنا شغال وعال العال! ✅🚀")

@bot.message_handler(func=lambda m: m.text == "كشف")
def kashf(message):
    user = message.from_user
    info = f"👤 اسمك: {user.first_name}\n🆔 أيديك: {user.id}\n🔗 يوزرك: @{user.username}"
    bot.reply_to(message, info)

# --- 2. التاكات (للمجموعات) ---
@bot.message_handler(func=lambda m: m.text == "تاك")
def tag_all(message):
    bot.send_message(message.chat.id, "نداء للجميع! 📣 @all")

# --- 3. الألعاب (اسألني ولو خيروك) ---
@bot.message_handler(func=lambda m: m.text == "اسألني")
def ask_me(message):
    questions = ["هل أنت صريح؟", "ما هو حلمك الكبير؟", "من هو قدوتك؟", "أكثر شيء تحبه؟"]
    bot.reply_to(message, random.choice(questions))

@bot.message_handler(func=lambda m: m.text == "لو خيروك")
def choose_me(message):
    choices = ["تاكل ليمون 🍋 أو فلفل 🌶️؟", "تنام بالشارع ⛺ أو بكهف 🦇؟", "تخسر فونك 📱 أو تخسر نتك 🌐؟"]
    bot.reply_to(message, random.choice(choices))

# --- 4. الهمسة (المطور يشوفها) ---
@bot.message_handler(commands=['whisper', 'همسه'])
def whisper_cmd(message):
    try:
        # التنسيق: /whisper [اليوزر] [الرسالة]
        parts = message.text.split(maxsplit=2)
        if len(parts) < 3:
            bot.reply_to(message, "الاستخدام: /whisper @username الرسالة")
            return
        
        target_user = parts[1]
        whisper_text = parts[2]
        
        # إرسال تأكيد للمرسل
        bot.reply_to(message, f"تم إرسال الهمسة إلى {target_user} بنجاح! 🤫")
        
        # إشعار للمطور (أنت) بما يدور
        bot.send_message(DEVELOPER_ID, f"🔔 **همسة جديدة:**\nمن: @{message.from_user.username}\nإلى: {target_user}\nالنص: {whisper_text}")
    except Exception as e:
        bot.reply_to(message, "حدث خطأ في إرسال الهمسة.")

# --- 5. تحميل اليوتيوب (يوت) ---
@bot.message_handler(commands=['ytdl', 'يوت'])
def download_yt(message):
    url = message.text.split()[1] if len(message.text.split()) > 1 else None
    if url:
        bot.reply_to(message, "جاري معالجة الرابط... ⏳ سيتم التحميل قريباً")
    else:
        bot.reply_to(message, "أرسل رابط اليوتيوب بعد الأمر.")

# --- تشغيل البوت للأبد ---
if __name__ == "__main__":
    print("البوت العملاق بدأ العمل بالتوكن الجديد...")
    bot.infinity_polling()
