# -*- coding: utf-8 -*-
from db import conn_lite3
# Aqui creas las funciones que trabajarán con el CommandHandler

def start (Update,contex):

    nombre = Update.effective_user.first_name

    Update.message.reply_text(
        text=f'Hola <b>{nombre}</b> soy un bot creado con python',
        parse_mode='html'
    )