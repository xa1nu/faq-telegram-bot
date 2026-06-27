import telebot
import os
from dotenv import load_dotenv
from telebot import types
from faq import FAQ

load_dotenv()
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        types.KeyboardButton("📅 Расписание"),
        types.KeyboardButton("💳 Оплата"),
        types.KeyboardButton("📚 Уровни"),
        types.KeyboardButton("📝 Домашка"),
        types.KeyboardButton("🏆 Сертификат"),
        types.KeyboardButton("🎁 Пробный урок"),
        types.KeyboardButton("👩‍🏫 Преподаватели"),
        types.KeyboardButton("📞 Контакты"),
        types.KeyboardButton("⭐️ Отзывы"),
        types.KeyboardButton("👥 Форматы")
    )
    return markup

def back_menu():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🏠 Главное меню", callback_data="home"))
    return markup

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id,
        f"👋 Привет, {message.from_user.first_name}!\n\n"
        "🎓 Добро пожаловать в LinguaFlow!\n"
        "Онлайн-школа английского языка\n\n"
        "Выбери тему — отвечу мгновенно! 👇",
        reply_markup=main_menu()
    )

@bot.message_handler(commands=["help"])
def help_cmd(message):
    bot.send_message(message.chat.id,
        "ℹ️ Как пользоваться ботом:\n\n"
        "• Нажимай кнопки внизу экрана\n"
        "• Или пиши вопрос своими словами\n"
        "• /start — главное меню\n"
        "• /contacts — наши контакты",
        reply_markup=main_menu()
    )

@bot.message_handler(commands=["contacts"])
def contacts_cmd(message):
    bot.send_message(message.chat.id,
        "📞 Контакты LinguaFlow:\n\n"
        "💬 Telegram: @linguaflow_admin\n"
        "📧 Email: info@linguaflow.ru\n"
        "🌐 Сайт: linguaflow.ru",
        reply_markup=main_menu()
    )

@bot.callback_query_handler(func=lambda call: call.data == "home")
def home_callback(call):
    bot.send_message(call.message.chat.id,
        "🏠 Главное меню\nВыбери тему 👇",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda m: True)
def answer(message):
    text = message.text.lower()
    for key, value in FAQ.items():
        if key in text:
            bot.send_message(
                message.chat.id,
                value,
                reply_markup=back_menu()
            )
            return
    bot.send_message(message.chat.id,
        "🤔 Не нашёл ответ на твой вопрос.\n\n"
        "Попробуй выбрать тему из меню 👇\n"
        "Или напиши нам: @linguaflow_admin",
        reply_markup=main_menu()
    )

bot.polling()