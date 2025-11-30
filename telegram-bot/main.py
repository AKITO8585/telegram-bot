import telebot
from telebot import types
from flask import Flask
from threading import Thread
import os
import time

TOKEN = os.environ.get("8564463627:AAG6vodvrzA9O99GjhPTLQhbDbnGvcoh868")
bot = telebot.TeleBot(8564463627:AAG6vodvrzA9O99GjhPTLQhbDbnGvcoh868)

app = Flask(name)

BAD_WORDS = ["کصننه", "مادرجنده", "خارکصه"]
SPAM_INTERVAL = 5
LINK_KEYWORDS = ["http://", "https://", ".com", ".ir"]
last_messages = {}
ADMIN_ID = 6438746647

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🤖 ربات مدیریت گروه فعال شد!")

@bot.message_handler(content_types=['new_chat_members'])
def welcome(message):
    for new_member in message.new_chat_members:
        bot.send_message(message.chat.id, f"سلام {new_member.first_name} خوش اومدی! 👋")

@bot.message_handler(func=lambda message: True)
def content_filter(message):
    if not message.text:
        return

    user_id = message.from_user.id
    now = time.time()

    if user_id in last_messages and now - last_messages[user_id] < SPAM_INTERVAL:
        bot.delete_message(message.chat.id, message.message_id)
        return
    last_messages[user_id] = now

    if any(word in message.text.lower() for word in BAD_WORDS):
        bot.delete_message(message.chat.id, message.message_id)
        return

    if any(keyword in message.text.lower() for keyword in LINK_KEYWORDS):
        bot.delete_message(message.chat.id, message.message_id)
        return

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def run_bot():
    print("🤖 ربات در حال اجرا روی Railway...")
    bot.infinity_polling()

if name == 'main':
    Thread(target=run_flask).start()
    Thread(target=run_bot).start()
