from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

DEPOSIT, RISK, SL = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Men lot hajmi kalkulyatoriman 💰\nHisobingizdagi depozitni kiriting ($):")
    return DEPOSIT

async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["deposit"] = float(update.message.text)
    await update.message.reply_text("Riski miqdorini kiriting ($):")
    return RISK

async def risk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["risk_dollars"] = float(update.message.text)
    await update.message.reply_text("Stop-lossni kiriting (pips):")
    return SL

async def sl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    deposit = context.user_data["deposit"]
    risk_dollars = context.user_data["risk_dollars"]
    sl_pips = float(update.message.text)

    # XAUUSD uchun 1 lot = $1 har 1 pipda (taxminan)
    lot = risk_dollars / (sl_pips * 10)  # har 10 pips uchun $10 yo'qotish

    await update.message.reply_text(
        f"💰 Depozit: ${deposit}\n"
        f"⚠️ Risk: ${risk_dollars:.2f}\n"
        f"📏 Stop: {sl_pips} pips\n\n"
        f"➡️ Lot hajmi: **{lot:.2f}**"
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bekor qilindi ❌")
    return ConversationHandler.END

def main():
    import os
    from telegram.ext import ApplicationBuilder

    BOT_TOKEN = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            DEPOSIT: [MessageHandler(filters.TEXT & ~filters.COMMAND, deposit)],
            RISK: [MessageHandler(filters.TEXT & ~filters.COMMAND, risk)],
            SL: [MessageHandler(filters.TEXT & ~filters.COMMAND, sl)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
