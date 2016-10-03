# -*- coding: utf-8 -*-

querymessages = {}


@bot.inline_handler(lambda query: len(query.query) is 0)
def default_query(inline_query):
  try:
    r = types.InlineQueryResultArticle('1', 'default', types.InputTextMessageContent('default'))
    bot.answer_inline_query(inline_query.id, [None], switch_pm_text="Switch")
  except Exception as e:
    print(e)
@bot.inline_handler(lambda query: query.query.split()[0] == 'echo')
def query_text(inline_query):
  try:
    if inline_query.query == "echo":
      r = types.InlineQueryResultArticle('1', 'Please enter a text!', types.InputTextMessageContent('I Love empty texts.'))
      bot.answer_inline_query(inline_query.id, [r])
    if len(inline_query.query.split()) > 1:
      try:
        r3 = types.InlineQueryResultArticle('3', 'Echo your message using HTML parse mode ;)', types.InputTextMessageContent(inline_query.query.replace("echo ", "", 1), parse_mode="HTML"))
        bot.answer_inline_query(inline_query.id, [r3], cache_time=1, is_personal=True)
      except:
        r3 = types.InlineQueryResultArticle('3', 'Error occured. One of your tags arent closed!', types.InputTextMessageContent("I forgot to close a tag."))
        bot.answer_inline_query(inline_query.id, [r3], cache_time=1, is_personal=True)
  except Exception as e:
    print(e)

@bot.inline_handler(lambda query: query.query.split()[0] == 'hideit')
def hideit_text(inline_query):
  try:
    if inline_query.query == "hideit":
      r = types.InlineQueryResultArticle('1', 'Please enter a text so I can hide it!', types.InputTextMessageContent('I Love empty texts.'))
      bot.answer_inline_query(inline_query.id, [r])
    if len(inline_query.query.split()) > 1:
      try:
        markupz = types.InlineKeyboardMarkup()
        markupid = types.InlineKeyboardButton("Show all cmds", callback_data='showit')
        markupz.add(markupid)
        print(str(markupz))
        query_text = {inline_query.id: inline_query.query.replace("hideit ", "", 1)}
        print(query_text)
        querymessages.update(query_text)
        r3 = types.InlineQueryResultArticle('3', 'Send hidden text!', types.InputTextMessageContent("❓❓❓"), reply_markup=markupz)
        bot.answer_inline_query(inline_query.id, [r3], cache_time=1, is_personal=True)
      except:
        r3 = types.InlineQueryResultArticle('3', 'Error occured.', types.InputTextMessageContent("Unexpected error occured."))
        bot.answer_inline_query(inline_query.id, [r3], cache_time=1, is_personal=True)
  except Exception as e:
    print(e)

