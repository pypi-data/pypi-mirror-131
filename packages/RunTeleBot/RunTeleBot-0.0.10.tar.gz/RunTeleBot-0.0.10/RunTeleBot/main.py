
from telegram.ext import Updater , CommandHandler , MessageHandler , Filters\
    ,CallbackQueryHandler

from MyHandlers import commands , callbackquerys , messages


TOKEN = 'token'
updater = Updater(TOKEN)
update=Updater
dp=updater.dispatcher

# start
dp.add_handler(CommandHandler('start',commands.start))


updater.start_polling()
print('run')
updater.idle()