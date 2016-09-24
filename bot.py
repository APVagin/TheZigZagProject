import datetime
import telebot
import logging
import sys
from telebot import types

reload(sys)  
sys.setdefaultencoding("utf-8")

execfile("locale.py")
execfile("config.py")


logfile = open("bot.log", "a")
time = datetime.datetime.now()
logfile.write("Bot Started: " + str(time) + " with ")
print("Bot started: " + str(time))

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  markup = types.ReplyKeyboardMarkup()
  lengthof = len(START_BUTTONS)
  countn = 0
  itembtn0 = None
  itembtn1 = None
  itembtn2 = None
  itembtn3 = None
  itembtn4 = None
  itembtn5 = None
  while (countn < lengthof):
    exec("itembtn" + str(countn) + " = types.KeyboardButton(START_BUTTONS[" + str(countn) + "])")
    countn = countn + 1
  
  markup.row(itembtn0, itembtn1, itembtn2)
  markup.row(itembtn3, itembtn4, itembtn5)
  if message.chat.type == "private":
    bot.reply_to(message, START_MSG.encode("utf-8"), reply_markup=markup)
  else:
    bot.reply_to(message, START_MSG.encode("utf-8"))

@bot.message_handler(commands=['test', 'toast'])
def send_test(message):
  bot.send_message(message.chat.id, TEST_MSG.encode("utf-8"))
  
@bot.message_handler(commands=['id'])
def send_id(message):
  username = message.from_user.first_name.encode("utf-8")
  userid = message.from_user.id
  reply_msg = ID_MSG.encode("utf-8")
  gpid = message.chat.id
  if message.chat.type == "supergroup":
    reply_msg = reply_msg + INGP_ID_MSG.encode("utf-8")
  elif message.chat.type == "group":
    reply_msg = reply_msg + INGP_ID_MSG.encode("utf-8")
  bot.reply_to(message, reply_msg.format(username, userid, gpid), parse_mode="Markdown")

@bot.message_handler(commands=['sendcontact'])
def send_test(message):
  bot.send_message(message.chat.id, SHARE_CONTACT_MSG.encode("utf-8"))
  

@bot.message_handler(commands=['echo'])
def echo_message(message):
  if SAFE_ECHO:
    if message.chat.type == "supergroup":
      bot.reply_to(message, NO_ECHO_IN_SUPERGP_MSG.encode("utf-8"))
      return
  if len(message.text.split()) < 2:
    bot.reply_to(message, ECHO_REPLY_MSG.encode("utf-8"), parse_mode="Markdown")
    return
  try:
    echo_msg = message.text.replace("/echo","",1)
    bot.reply_to(message, echo_msg)
  except:
    bot.send_message(messsage.chat.id, ERROR_MSG.encode("utf-8"))
  
def message_replier(messages):
  for message in messages:
    if message.text in reply_message_list:
      bot.reply_to(message, reply_message_list.get(message.text), parse_mode="Markdown")

@bot.message_handler(func=lambda message: True, content_types=['new_chat_member'])
def user_greet(message):
  if GP_GREETING:
    if message.new_chat_member.id != bot.get_me().id:
      name = message.new_chat_member.first_name
      title = message.chat.title
      bot.send_message(message.chat.id, GP_GREETING_MSG.format(name,title).encode("utf-8"), parse_mode='Markdown')
  
  if message.new_chat_member.id == bot.get_me().id:
    inviter = message.from_user.id
    if inviter not in ADMINS_IDS:
      bot.send_message(message.chat.id, NON_ADMIN_ADDED_BOT_MSG.encode("utf-8"))
      bot.leave_chat(message.chat.id)
    else:
      bot.send_message(message.chat.id, BOT_JOINED_MSG)
  
@bot.message_handler(func=lambda message: True, content_types=['left_chat_member'])
def user_greet(message):
  if GP_FAREWELL:
    name = message.left_chat_member.first_name
    title = message.chat.title
    bot.send_message(message.chat.id, GP_FAREWELL_MSG.format(name,title).encode("utf-8"), parse_mode='Markdown')
  
@bot.message_handler(func=lambda m: True, content_types=['contact'])
def contact_forwarder(contact):
  if contact.chat.type == "private":
    bot.send_message(SUDO_ID, CONTACT_RECIEVED_MSG.encode("utf-8"))
    bot.forward_message(SUDO_ID, contact.chat.id, contact.message_id)
    bot.reply_to(contact, CONTACT_FORWARDED_MSG.encode("utf-8"))

logger = telebot.logger
if DEEP_LOGGING:
  print("Debugging enabled.")
  logfile.write("debugging enabled. \n")
  telebot.logger.setLevel(logging.DEBUG)
else:
  logfile.write("debugging disabled. \n")
  print("Debugging disabled.")

if REPLIER:
  bot.set_update_listener(message_replier)

logfile.close()
bot.polling(none_stop=True, interval=0, timeout=3)
