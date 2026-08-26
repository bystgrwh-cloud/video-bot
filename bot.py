import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
MY_ID = int(os.environ.get("MY_ID", "0"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! 👋\nویدیو بفرست، لینک مستقیم میدم.")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != MY_ID:
        await update.message.reply_text("⛔ دسترسی نداری")
        return
    
    if update.message.video:
        f = update.message.video
    elif update.message.document:
        f = update.message.document
    else:
        await update.message.reply_text("❌ فقط ویدیو/فایل بفرست")
        return
    
    file = await f.get_file()
    msg = await update.message.reply_text("⏳ در حال ساخت لینک...")
    
    await msg.edit_text(
        f"✅ لینک مستقیم:\n\n"
        f"🔗 {file.file_path}\n\n"
        f"💾 {f.file_size / 1024 / 1024:.1f} MB\n\n"
        f"💡 تو VLC باز کن"
    )

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.VIDEO | filters.Document.ALL, handle))
app.run_polling()
