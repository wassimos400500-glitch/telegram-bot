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

flags = {
    "🇩🇿": "الجزائر",
    "🇲🇦": "المغرب",
    "🇯🇵": "اليابان",
    "🇧🇷": "البرازيل",
    "🇫🇷": "فرنسا",
    "🇹🇷": "تركيا",
    "🇪🇬": "مصر",
    "🇨🇦": "كندا",
    "🇰🇷": "كوريا الجنوبية",
    "🇮🇹": "إيطاليا",
    "🇩🇪": "ألمانيا",
    "🇪🇸": "إسبانيا",
    "🇬🇧": "المملكة المتحدة",
    "🇺🇸": "الولايات المتحدة",
    "🇸🇦": "السعودية"
}

capitals = {
    "الجزائر": "الجزائر",
    "المغرب": "الرباط",
    "اليابان": "طوكيو",
    "البرازيل": "برازيليا",
    "فرنسا": "باريس",
    "تركيا": "أنقرة",
    "مصر": "القاهرة",
    "كندا": "أوتاوا",
    "كوريا الجنوبية": "سيول",
    "إيطاليا": "روما",
    "ألمانيا": "برلين",
    "إسبانيا": "مدريد",
    "المملكة المتحدة": "لندن",
    "الولايات المتحدة": "واشنطن",
    "السعودية": "الرياض"
}async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text in replies:
        await update.message.reply_text(replies[text])

    elif text == "اية":
        await update.message.reply_text(random.choice(verses))

    elif text == "اعلام":
        flag = random.choice(list(flags.keys()))
        context.user_data["flag_answer"] = flags[flag]
        await update.message.reply_text(flag)

    elif "flag_answer" in context.user_data:
        answer = context.user_data["flag_answer"]
        if text == answer:
            await update.message.reply_text("برافو ✅")
        else:
            await update.message.reply_text(f"خطأ ❌ الإجابة هي {answer}")
        del context.user_data["flag_answer"]

    elif text == "عواصم":
        country = random.choice(list(capitals.keys()))
        context.user_data["capital_answer"] = capitals[country]
        await update.message.reply_text(f"ما ع
app.run_polling()
