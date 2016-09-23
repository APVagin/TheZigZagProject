import datetime
import telebot
import logging
from telebot import types


time = datetime.datetime.now()
print("Bot started: " + str(time))

# CONFIG
TOKEN = '116144035:AAHVDjt5VX-5bKGGrbtw6QJPEZF4reJcIjc' # BOT TOKEN
LOGGING = False # FOR DEBUGGING PURPOSES ONLY
REPLIER = True # Lol.. a simple reply-to-message system xD (using dictionaries)

#REPLY MESSAGES
reply_message_list = {"salam": "slm",
  "hi": "aleyke hi",
  "hello": "dorood",
}
# END OF CONFIG

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  markup = types.ReplyKeyboardMarkup()
  itembtna = types.KeyboardButton('/start')
  itembtnv = types.KeyboardButton('/help')
  markup.row(itembtna, itembtnv)
  bot.reply_to(message, "Hey, Hi!", reply_markup=markup)

@bot.message_handler(commands=['test', 'toast'])
def send_test(message):
  bot.send_message(message.chat.id, "LoL Test Msg")

@bot.message_handler(commands=['echo'])
def echo_message(message):
  # To disable this function, just comment theese three below lines
  if message.chat.type == "supergroup":
    bot.reply_to(message, "Unfortunately I wont reply to messages sent in a supergroup to prevent spamming.")
    return
  if len(message.text.split()) < 2:
    bot.reply_to(message, "Please enter a text so I reply to it!")
    return
  try:
    echo_msg = message.text.replace("/echo","",1)
    bot.reply_to(message, echo_msg)
  except:
    bot.send_message(messsage.chat.id, "Error occured.")
  
def message_replier(messages):
  for message in messages:
    if message.text in reply_message_list:
      bot.reply_to(message, reply_message_list.get(message.text))


logger = telebot.logger
if LOGGING:
  print("Logging enabled.")
  telebot.logger.setLevel(logging.DEBUG)
else:
  print("Logging disabled.")

if REPLIER:
  bot.set_update_listener(message_replier)

bot.polling(none_stop=True, interval=0, timeout=3)
