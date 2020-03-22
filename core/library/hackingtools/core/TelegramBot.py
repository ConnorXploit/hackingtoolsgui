try:
    import telebot as __telebot
    from telebot import types
    import time as __time
    import hackingtools as ht
    import ast as __ast
    
    __bot_name__ = ht.core.Config.getConfig(parentKey='core', key='TelegramBot', subkey='bot-name')
    __bot_token__ = ht.core.Config.getConfig(parentKey='core', key='TelegramBot', subkey='bot-token')
    bot = None

    __crossIcon__ = u"\u274C"

    try:
        bot = __telebot.TeleBot(__bot_token__)
    except:
        pass

    @bot.message_handler(commands=['start'])
    def handle_command_adminwindow(message):
        modules = ht.getModulesNames()

        markup = types.InlineKeyboardMarkup()

        modules_list_3 = ht.Utils.groupListByLength(modules, 3) 
        
        # [ 
        #     ['ht_shodan','ht_*','ht_*'],
        #     ['ht_*','ht_*','ht_*'],
        #     ['ht_*','ht_*','ht_*'] ,
        #     ['ht_*','ht_*'] 
        # ]

        # ['value', 'ht_shodan', 'osint']

        for line in modules_list_3:
            if len(line) == 3:
                markup.add(types.InlineKeyboardButton(text=line[0], callback_data="['value', '" + line[0] + "', '" + ht.getModuleCategory(line[0]) + "']"),
                types.InlineKeyboardButton(text=line[1], callback_data="['value', '" + line[1] + "', '" + ht.getModuleCategory(line[1]) + "']"),
                types.InlineKeyboardButton(text=line[2], callback_data="['value', '" + line[2] + "', '" + ht.getModuleCategory(line[2]) + "']"))
            elif len(line) == 3:
                markup.add(types.InlineKeyboardButton(text=line[0], callback_data="['value', '" + line[0] + "', '" + ht.getModuleCategory(line[0]) + "']"),
                types.InlineKeyboardButton(text=line[1], callback_data="['value', '" + line[1] + "', '" + ht.getModuleCategory(line[1]) + "']"))
            else:
                markup.add(types.InlineKeyboardButton(text=line[0], callback_data="['value', '" + line[0] + "', '" + ht.getModuleCategory(line[0]) + "']"))

        bot.send_message(chat_id=message.chat.id, text="Here you have the modules:", reply_markup=markup)
        
    @bot.callback_query_handler(lambda q: q.message.chat.type == "private")
    def private_query(query):
        try:
            if (query.data.startswith("['value'")):
                moduleName = __ast.literal_eval(query.data)[1]
                category = __ast.literal_eval(query.data)[2]

                functions = '\n'.join( ht.getFunctionsNamesFromModule(moduleName) )

                bot.answer_callback_query(callback_query_id=query.id, show_alert=True, text=functions)
                
            bot.edit_message_reply_markup(query.message.chat.id, query.message.message_id)
        except Exception as e:
            bot.answer_callback_query(callback_query_id=query.id, show_alert=True, text=str(e))

    bot.polling()
except:
    try:
        bot.stop_polling()
    except:
        pass