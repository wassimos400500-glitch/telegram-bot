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
