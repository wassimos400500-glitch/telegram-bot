from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import os

TOKEN= "8766911595:AAH1u67LIcIFwbal5wznLXxxEso21Mbak0E"

responses = {
    "واه": "متلعبهاش وهراني يا واحد القسنطيني",
    "مهم": "صايي روح برب نبقاو نهدروا برك",
    "علاه": "وش دخلك",
    "وسيم": "my father"
}

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text in responses:
        await update.message.reply_text(responses[text])

app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, reply))

print("Bot started...")
app.run_polling()
import os
import random
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TOKEN = 8766911595:AAH1u67LIcIFwbal5wznLXxxEso21Mbak0E
replies = {
    "برب": "شلقماتك برب؟",
    "لا": "لا",
    "افا": "لااااااااااااا",
    "هيه": "برافو هك أك قسنطيني",
    "تم": "يب",
    "شكرا": "زعما مأدب",
    "كافي": "يحيى؟",
    "ماتش؟": "علاه روح صلي",
    "معز": "نيوزر"
}

verses = [
    "﴿إِنَّ مَعَ الْعُسْرِ يُسْرًا﴾",
    "﴿وَقُل رَّبِّ زِدْنِي عِلْمًا﴾",
    "﴿إِنَّ اللَّهَ مَعَ الصَّابِرِينَ﴾",
    "﴿وَاللَّهُ خَيْرُ الرَّازِقِينَ﴾"
]

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if text in replies:
        await update.message.reply_text(replies[text])

    elif text == "اية":
        await update.message.reply_text(random.choice(verses))

    else:
        await update.message.reply_text("لم أفهم رسالتك")


app = Application.builder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT, message_handler))

app.run_polling()flags = [
    "🇯🇵 اليابان",
    "🇧🇷 البرازيل",
    "🇫🇮 فنلندا",
    "🇵🇹 البرتغال",
    "🇰🇷 كوريا الجنوبية",
    "🇳🇴 النرويج",
    "🇮🇸 آيسلندا",
    "🇲🇾 ماليزيا",
    "🇻🇳 فيتنام",
    "🇷🇴 رومانيا",
    "🇲🇦 المغرب",
    "🇩🇿 الجزائر",
    "🇹🇷 تركيا",
    "🇨🇦 كندا"
]

capitals = [
    "ما عاصمة اليابان؟",
    "ما عاصمة البرازيل؟",
    "ما عاصمة البرتغال؟",
    "ما عاصمة تركيا؟",
    "ما عاصمة كندا؟",
    "ما عاصمة المغرب؟",
    "ما عاصمة الجزائر؟",
    "ما عاصمة كوريا الجنوبية؟",
    "ما عاصمة النرويج؟",
    "ما عاصمة ماليزيا؟"
]

countries = [
    "طوكيو 🇯🇵",
    "برازيليا 🇧🇷",
    "لشبونة 🇵🇹",
    "أنقرة 🇹🇷",
    "أوتاوا 🇨🇦",
    "الرباط 🇲🇦",
    "الجزائر 🇩🇿",
    "سيول 🇰🇷",
    "أوسلو 🇳🇴",
    "كوالالمبور 🇲🇾"
]
