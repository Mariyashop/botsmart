import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import openai
import os

# تنظیم توکن‌ها
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# پاسخ به پیام‌ها
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.strip()

    if user_message.lower().startswith("نینی بات"):
        question = user_message[len("نینی بات"):].strip()

        if not question:
            await update.message.reply_text("سوالت رو بعد از «سوال دارم» بنویس دیگه!", reply_to_message_id=update.message.message_id)
            return

        await update.message.reply_text(
            "🥺 من نینی هستم... لطفاً منو اذیت نکنید! 👶🍼 منو آمون بزرگ خلق کرده، ناناحتم... سوالتو بپرس ببینم 😢",
            reply_to_message_id=update.message.message_id
    )

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

        # پاسخ به سوال - ریپلای به پیام کاربر
        await update.message.reply_text(answer, reply_to_message_id=update.message.message_id)

# اجرای ربات
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
