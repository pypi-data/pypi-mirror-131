
from pyrogram.types import InlineKeyboardMarkup , InlineKeyboardButton
from db import conn_lite3

# Archivo para los comandos - filters.command(['nombre_comando'])

def start (client,message):
	name = message.from_user.first_name

	message.reply_text(
		text=f'Bienvenido <b>{name}</b> soy un bot hecho en python',
		parse_mode="html",
		reply_markup=InlineKeyboardMarkup([
			[InlineKeyboardButton('editar mensaje',callback_data='editar')]
			]))