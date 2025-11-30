import telebot
from telebot import types
from flask import Flask
from threading import Thread
import time
import os

# ====== توکن ربات ======
TOKEN = os.environ.get("8564463627:AAG6vodvrzA9O99GjhPTLQhbDbnGvcoh868")  # توکن را در Railway به عنوان Environment Variable وارد کن
bot = telebot.TeleBot(8564463627:AAG6vodvrzA9O99GjhPTLQhbDbnGvcoh868)

# ====== تنظیمات ======
BAD_WORDS = ["فحش1", "فحش2", "فحش3"]  # لیست فحش‌ها
SPAM_INTERVAL = 5
LINK_KEYWORDS = ["http://", "https://", ".com", ".ir"]
last_messages = {}
ADMIN_ID = 6438746647  # آیدی مدیر اصلی

# ====== خوش آمدگویی ======
@bot.message_handler(content_types=['new_chat_members'])
def welcome(message):
    for new_member in message.new_chat_members:
        bot.send_message(message.chat.id, f"سلام {new_member.first_name} خوش اومدی! 👋")

# ====== حذف فحش و لینک ======
@bot.message_handler(func=lambda message: True)
def content_filter(message):
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

# ====== حذف عکس و ویدیو ======
@bot.message_handler(content_types=['photo', 'video', 'sticker', 'animation'])
def delete_media(message):
    bot.delete_message(message.chat.id, message.message_id)

# ====== پنل مدیریت دکمه‌ای ======
@bot.message_handler(commands=['panel'])
def panel(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "شما اجازه دسترسی به پنل را ندارید!")
        return

    markup = types.InlineKeyboardMarkup(row_width=2)
    mute_btn = types.InlineKeyboardButton("سکوت 🔇", callback_data="mute")
    ban_btn = types.InlineKeyboardButton("بن 🚫", callback_data="ban")
    markup.add(mute_btn, ban_btn)
    bot.send_message(message.chat.id, "پنل مدیریت:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    chat_id = call.message.chat.id
    if call.data == "mute":
        bot.send_message(chat_id, "برای سکوت کردن، دستور زیر را استفاده کنید:\n/mute (ریپلای روی پیام)")
    elif call.data == "ban":
        bot.send_message(chat_id, "برای بن کردن، دستور زیر را استفاده کنید:\n/ban (ریپلای روی پیام)")

@bot.message_handler(commands=['mute'])
def mute_user(message):
    if message.from_user.id != ADMIN_ID: return
    if not message.reply_to_message: return
    user_id = message.reply_to_message.from_user.id
    bot.restrict_chat_member(message.chat.id, user_id, can_send_messages=False)
    bot.reply_to(message, f"{message.reply_to_message.from_user.first_name} سکوت شد! 🔇")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.from_user.id != ADMIN_ID: return
    if not message.reply_to_message: return
    user_id = message.reply_to_message.from_user.id
    bot.ban_chat_member(message.chat.id, user_id)
    bot.reply_to(message, f"{message.reply_to_message.from_user.first_name} بن شد! 🚫")

# ====== Web Server برای همیشه آنلاین بودن ======
app = Flask('')

@app.route('/')
def home():
    return "Bot is running"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

Thread(target=run).start()

# ====== اجرای ربات ======
bot.infinity_polling()
