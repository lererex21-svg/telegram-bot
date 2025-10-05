import telebot

TOKEN = "8366398067:AAESiea7a2XTb7frVhDXUxFBJ14kSZyEoOg"  # masalan: 8194345051:AAEOvCjpOU3hyXbPrOW3AtR8BHoL9epMunc
bot = telebot.TeleBot(TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "💰 Risk Kalkulyatori\n\nHisob hajmini kiriting (masalan: 5000):")
    bot.register_next_step_handler(message, get_account_size)

def get_account_size(message):
    try:
        account_size = float(message.text)
        user_data[message.chat.id] = {'account_size': account_size}
        bot.send_message(message.chat.id, "💵 Risk miqdorini kiriting ($ da, masalan: 100):")
        bot.register_next_step_handler(message, get_risk_dollars)
    except ValueError:
        bot.send_message(message.chat.id, "❌ Noto‘g‘ri raqam. Iltimos, faqat raqam kiriting.")
        bot.register_next_step_handler(message, get_account_size)

def get_risk_dollars(message):
    try:
        risk_dollars = float(message.text)
        user_data[message.chat.id]['risk_dollars'] = risk_dollars
        bot.send_message(message.chat.id, "📉 Stop-loss hajmini kiriting (pipda, masalan: 10):")
        bot.register_next_step_handler(message, get_stop_loss)
    except ValueError:
        bot.send_message(message.chat.id, "❌ Iltimos, faqat raqam kiriting.")
        bot.register_next_step_handler(message, get_risk_dollars)

def get_stop_loss(message):
    try:
        stop_loss = float(message.text)
        user_data[message.chat.id]['stop_loss'] = stop_loss
        bot.send_message(message.chat.id, "📊 Siz qaysi juftlikni ishlatyapsiz?\nMasalan: XAUUSD, EURUSD...")
        bot.register_next_step_handler(message, get_pair)
    except ValueError:
        bot.send_message(message.chat.id, "❌ Iltimos, faqat raqam kiriting.")
        bot.register_next_step_handler(message, get_stop_loss)

def get_pair(message):
    pair = message.text.upper()
    user_data[message.chat.id]['pair'] = pair
    calculate_lot(message)

def calculate_lot(message):
    data = user_data[message.chat.id]
    account_size = data['account_size']
    risk_dollars = data['risk_dollars']
    stop_loss = data['stop_loss']
    pair = data['pair']

    # Pip qiymatini aniqlash
    if "JPY" in pair:
        pip_value = 0.01
    else:
        pip_value = 0.1

    # XAUUSD uchun alohida
    if pair == "XAUUSD":
        pip_value = 1

    # Lot hisoblash formulasi
    lot = risk_dollars / (stop_loss * pip_value * 10)

    bot.send_message(
        message.chat.id,
        f"✅ Hisoblash tugadi!\n\n"
        f"💼 Hisob hajmi: ${account_size:,.2f}\n"
        f"💵 Risk: ${risk_dollars:,.2f}\n"
        f"📉 Stop-loss: {stop_loss} pip\n"
        f"💱 Juftlik: {pair}\n\n"
        f"📈 Lot hajmi: {lot:.2f}"
    )

    bot.send_message(message.chat.id, "Yana hisoblash uchun /start ni bosing 🔁")

print("🤖 Bot ishga tushdi...")
bot.polling(non_stop=True)
