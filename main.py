import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from rag import RAGSystem

# Настройка логирования
logging.basicConfig(filename="bot.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Токен Telegram бота
TOKEN = "YOUR_TELEGRAM_TOKEN_HERE"

# Инициализация RAG
rag_system = RAGSystem(chroma_dir="./chroma_db")

def start(update, context):
    keyboard = [
        [InlineKeyboardButton("Оформить карту", url="https://tbank.ru/kassa/form/partner/")],
        [InlineKeyboardButton("Узнать лимиты", callback_data="limits")],
        [InlineKeyboardButton("Связаться с поддержкой", url="https://tbank.ru/support/")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "👋 *Привет!* Я TinkHelper. Задай вопрос или выбери действие ниже.\nПримеры: 'Как посмотреть лимиты счета?'",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )
    logging.info(f"User {update.message.from_user.id}: /start")

def help_command(update, context):
    update.message.reply_text(
        "📖 *Помощь по TinkHelper*\n\n"
        "Я отвечаю на вопросы о продуктах T-Bank. Примеры:\n"
        "- Как посмотреть лимиты счета?\n"
        "- Какие лимиты на переводы?\n"
        "- Как оформить кредитную карту?\n\n"
        "Используй команды:\n"
        "/start — начать\n"
        "/help — помощь\n\n"
        "Задай вопрос или выбери действие в меню!",
        parse_mode="Markdown"
    )
    logging.info(f"User {update.message.from_user.id}: /help")

def button_callback(update, context):
    query = update.callback_query
    if query.data == "limits":
        context.bot.send_message(
            chat_id=query.message.chat_id,
            text="📊 Задайте вопрос про лимиты, например: 'Как посмотреть лимиты счета?'"
        )
    query.answer()
    logging.info(f"User {query.from_user.id}: Button {query.data}")

def handle_message(update, context):
    user_id = update.message.from_user.id
    query = update.message.text
    logging.info(f"User {user_id}: {query}")

    # Персонализация: проверка контекста
    if "last_query" not in context.user_data:
        context.user_data["last_query"] = ""
    if "счёт" in query.lower() and "счёт" in context.user_data["last_query"].lower():
        response = "Вы уже спрашивали про счёт. Хотите узнать про лимиты или открыть новый счёт?"
        buttons = [
            {"text": "Узнать лимиты", "url": "https://tbank.ru/app/check-limits"},
            {"text": "Открыть счёт", "url": "https://tbank.ru/kassa/form/partner/"}
        ]
    else:
        response, buttons = rag_system.get_response(query, use_llm=False)

    context.user_data["last_query"] = query

    # Формируем клавиатуру
    keyboard = [[InlineKeyboardButton(btn["text"], url=btn["url"])] for btn in buttons]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем ответ
    update.message.reply_text(response, parse_mode="Markdown", reply_markup=reply_markup)
    logging.info(f"Response to {user_id}: {response}")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(CallbackQueryHandler(button_callback))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()