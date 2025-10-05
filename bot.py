from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Bot is running on Render ✅"

# --- Telegram part ---
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalomu alaykum! 👋 Men lot kalkulyatoriman.\n\nBalansingizni yozing 💰:")
    user_data[update.effective_chat.id] = {"step": "balance"}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text.strip()

    if chat_id not in user_data:
        await update.message.reply_text("Напиши /start, чтобы начать 🙂")
        return

    data = user_data[chat_id]

    if data["step"] == "balance":
        try:
            data["balance"] = float(text)
            data["step"] = "risk"
            await update.message.reply_text("Endi risk summasini yozing $ 💵 (masalan, 50):")
        except:
            await update.message.reply_text("Son yozing, masalan 1000")

    elif data["step"] == "risk":
        try:
            data["risk_money"] = float(text)
            data["step"] = "sl"
            await update.message.reply_text("Nechi pips stop loss qoyasiz? 📉 (masalan, 10):")
        except:
            await update.message.reply_text("Son yozing, masalan 50")

    elif data["step"] == "sl":
        try:
            data["sl"] = float(text)
            # --- Расчёт ---
            balance = data["balance"]
            risk_money = data["risk_money"]
            sl_pips = data["sl"]

            pip_value = 10  # Для XAUUSD 1 лот = $1/pip
            lot_size = round(risk_money / (sl_pips * pip_value), 2)

            await update.message.reply_text(
                f"💰 Balans: {balance}\n⚠️ Risk: ${risk_money:.2f}\n📉 SL: {sl_pips} pips\n\n✅ Sizning LOTingiz: {lot_size}"
            )
            del user_data[chat_id]
        except:
            await update.message.reply_text("Ошибка ввода. Попробуй снова.")

def run_flask():
    app_flask.run(host="0.0.0.0", port=10000)

def run_telegram():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    Thread(target=run_flask).start()
    run_telegram()
