import logging
import os
import torch
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# بارگیری مدل DistilBERT (مدل سبک و کم حجم)
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased")
model.eval()
if torch.cuda.is_available():
    model.to("cuda")

# گرفتن توکن از محیط
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
PORT = int(os.getenv("PORT", 8080))  # تنظیم پورت از محیط، پیش‌فرض پورت 8080

# تولید پاسخ
def generate_response(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    input_ids = inputs.input_ids.to(model.device)
    with torch.no_grad():
        outputs = model(input_ids)
    # نتیجه‌گیری مدل می‌تواند برای پاسخ‌ها استفاده شود
    response = tokenizer.decode(outputs.logits.argmax(dim=-1), skip_special_tokens=True)
    return response

# پاسخ به پیام‌ها
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.strip()

    # پیام شخصیت‌دار نینی بات
    await update.message.reply_text(
        "🥺 من نینی هستم... لطفاً منو اذیت نکنید! 👶🍼 منو آمون بزرگ خلق کرده، ناناحتم... سوالتو بپرس ببینم 😢",
        reply_to_message_id=update.message.message_id
    )

    # حالا هر پیامی که ارسال بشه (سوالات مختلف) بهش پاسخ می‌ده
    question = user_message
    try:
        response = generate_response(question)  # جواب به سوال کاربر
    except Exception as e:
        response = f"مشکلی پیش اومد: {e}"

    # ریپلای به پیام اصلی کاربر
    await update.message.reply_text(response, reply_to_message_id=update.message.message_id)

# راه‌اندازی ربات
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # فیلتر به گونه‌ای تنظیم شده که به همه پیام‌ها جواب می‌ده
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # سرویس رو روی پورت مشخص شده اجرا کن
    app.run_polling(port=PORT)  # پورت رو در اینجا مشخص کردیم
