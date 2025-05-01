import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import openai
import os

# تنظیم توکن‌ها
TELEGRAM_TOKEN = "7092573468:AAEP1YTLNKsWsSm7oERQbP8OA3pr4O1zBcQ"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # حتماً تو Railway ست کن

openai.api_key = OPENAI_API_KEY

# پاسخ به پیام‌ها
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.strip()

    if user_message.lower().startswith("سوال دارم"):
        question = user_message[len("سوال دارم"):].strip()

        if not question:
            await update.message.reply_text("سوالت رو بعد از «سوال دارم» بنویس دیگه!")
            return

        # پیام اولیه طنز
        await update.message.reply_text("والا منو امون بزرگ خلق کرد، خودمم نمی‌دونم چرا درست شدم بی‌تقصیرم!\nسوالتو بپرس:")

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": question}],
                max_tokens=1000,
                temperature=0.7
            )
            answer = response.choices[0].message.content.strip()
        except Exception as e:
            answer = f"مشکلی پیش اومد: {e}"

        await update.message.reply_text(answer)

# اجرای ربات
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
