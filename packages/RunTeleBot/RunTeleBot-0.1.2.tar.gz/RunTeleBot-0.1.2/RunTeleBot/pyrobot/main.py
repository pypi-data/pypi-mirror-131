# -*- coding: utf-8 -*-
from pyrogram import Client , filters
from pyrogram.handlers import MessageHandler , CallbackQueryHandler

# importamos nuestros módulos
from MyHandlers import commands , callbackquerys , messages

pyrobot = Client('my_pyrobot',api_id='apiid',api_hash='apihash',bot_token='TOKEN')

# start
pyrobot.add_handler(MessageHandler(commands.start , filters.command(['start']) ))
# editar mensaje
pyrobot.add_handler(CallbackQueryHandler(callbackquerys.editar , 'editar' ))

pyrobot.run()