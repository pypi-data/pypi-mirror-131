
from db import conn_lite3
# Archivo para el CallbackQueryHandler


def editar (client,callback_query):

    callback_query.message.edit_text("Mensaje Editado")