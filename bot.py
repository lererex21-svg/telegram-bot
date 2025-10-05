from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

BOT_TOKEN = "8366398067:AAESiea7a2XTb7frVhDXUxFBJ14kSZyEoOg"  # bu yerga o'z bot tokeningni yoz

# holatlar
BALANCE, RISK, STOP = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! Men XAUUSD uchun lot kalkulyatoriman 💰\n"
        "Keling, hisoblaymiz.\n\n"
        "💵 Avvalo balansni kiriting (misol: 300):"
    )
    return BALANCE

async def balance_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        balance = float(update.message.text)
        context.user_data["balance"] = balance
        await update.message.reply_text("⚠️ Riskni $ da kiriting (misol: 45):")
        return RISK
    except ValueError:
        await update.message.reply_text("Iltimos, raqam kiriting. Masalan: 300")
        return BALANCE

async def risk_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        risk = float(update.message.text)
        context.user_data["risk"] = risk
        await update.message.reply_text("📉 Stop lossni pipsda kiriting (misol: 20):")
        return STOP
    except ValueError:
        await update.message.reply_text("Iltimos, raqam kiriting. Masalan: 45")
        return RISK

async def stop_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        stop = float(update.message.text)
        balance = context.user_data["balance"]
        risk = context.user_data["risk"]

        # 1 pips = $1 (1 lot uchun), ammo XAUUSD uchun /10
        lot_size = (risk / (stop * 1)) / 10

        await update.message.reply_text(
            f"✅ Hisoblash tugadi:\n\n"
            f"💵 Balans: {balance}$\n"
            f"⚠️ Risk: {risk}$\n"
            f"📉 Stop: {stop} pips\n"
            f"📊 Lot hajmi: {lot_size:.2f} lot"
        )
        return ConversationHandler.END

    except ValueError:
        await update.message.reply_text("Iltimos, raqam kiriting. Masalan: 20")
        return STOP

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bekor qilindi ❌")
    return ConversationHandler.END

app = ApplicationBuilder().token(BOT_TOKEN).build()

conv = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        BALANCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, balance_input)],
        RISK: [MessageHandler(filters.TEXT & ~filters.COMMAND, risk_input)],
        STOP: [MessageHandler(filters.TEXT & ~filters.COMMAND, stop_input)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

app.add_handler(conv)

if __name__ == "__main__":
    app.run_polling()
