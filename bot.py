from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import random

TOKEN = "8766911595:AAH1u67LIcIFwbal5wznLXxxEso21Mbak0E"

responses = {
    "السلام عليكم": "وعليكم السلام ورحمة الله وبركاته",
    "واه": "متلعبهاش وهراني يا واحد القسنطيني",
    "مهم": "صايي روح برب نبقاو نهدروا برك",
    "علاه": "وش دخلك",
    "وسيم": "my father",
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


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if text in responses:
        await update.message.reply_text(responses[text])


app = Application.builder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT, message_handler))

print("Bot started...")

app.run_polling()
