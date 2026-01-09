import telebot
import random

# التوكن الخاص بك
TOKEN = "8303634172:AAFAu8zC7RWFPRSOOXM_lYAflVKt489stKw"
bot = telebot.TeleBot(TOKEN)

# سطر سحري لمسح أي تعليق قديم
bot.remove_webhook()

@bot.message_handler(func=lambda m: True)
def all_messages(message):
    text = message.text
    if text == "البوت":
        bot.reply_to(message, "شغال يا بطل! ✅")
    elif text == "لو خيروك":
        bot.reply_to(message, random.choice(["تاكل فلفل 🌶️", "تاكل ليمون 🍋"]))
    elif text == "كشف":
        bot.reply_to(message, f"أيديك: {message.from_user.id}")
    else:
        bot.reply_to(message, f"وصلتني رسالتك: {text}")

if __name__ == "__main__":
    print("بدأ البوت بالعمل فعلياً...")
    bot.infinity_polling()
