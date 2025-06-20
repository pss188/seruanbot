import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ========== CONFIGURASI ==========
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Ambil dari Railway Variables
WEBHOOK_URL = os.getenv("https://diligent-charisma.railway.app", "")  # Optional untuk webhook
PORT = int(os.getenv("PORT", 8443))  # Port default Railway
WEBAPP_URL = "https://rebrand.ly/bbtop"  # Ganti dengan URL website Anda
LIVECHAT_URL = "https://direct.lc.chat/19031753/"
# ========== HANDLER COMMAND ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Kirim gambar dari folder assets
        with open("assets/hamster.jpg", "rb") as photo:
            await update.message.reply_photo(
                photo=photo,
                caption="🎮 **BANGBOS SITUS PALING GACOR** - Mainkan Akun Gacormu Sekarang!",
                parse_mode="Markdown"
            )
        
        # Buat tombol
        keyboard = [
            [InlineKeyboardButton("▶️ PLAY NOW", url=WEBAPP_URL)],
            [InlineKeyboardButton("📚 LIVECHAT", url=LIVECHAT_URL)]
        ]
        await update.message.reply_text(
            "Pilih tombol di bawah:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception as e:
        print(f"Error di handler /start: {e}")
        await update.message.reply_text("⚠️ Maaf, terjadi error. Silakan coba lagi.")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f"Anda memilih: {query.data}")

# ========== SETUP BOT ==========
def main():
    if not TOKEN:
        print("ERROR: Token tidak ditemukan!")
        print("Pastikan TELEGRAM_BOT_TOKEN sudah di-set di Railway Variables")
        exit(1)

    # Buat aplikasi bot
    application = Application.builder().token(TOKEN).build()
    
    # Tambahkan handler
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Jalankan bot
    if WEBHOOK_URL:  # Jika menggunakan webhook (production)
        print("Running in WEBHOOK mode")
        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            webhook_url=f"{WEBHOOK_URL}/{TOKEN}"
        )
    else:  # Mode polling (development)
        print("Running in POLLING mode")
        application.run_polling()

if __name__ == "__main__":
    main()
