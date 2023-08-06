# -*- coding: utf-8 -*-
import os 
import pathlib

def ptbot ():

    bot_name = input('Entre el nombre de su bot de telegram: ')
    if bot_name == '':
        bot_name = 'miBot'
    
    token = input('Entre el token del bot : ')
    if token == '':
        token = 'TOKEN'

    HERE = pathlib.Path(__file__).parent
    
    bot_dir = f'{bot_name}/'
    handlers_dir = f'{bot_dir}MyHandlers/'

    
    if os.path.exists(bot_dir):
        
        print(f'Ya exite un proyecto llamado {bot_name}')
    
    else :
        
        # Crear carpetas para el nuevo proyecto
 
        os.mkdir(bot_name)
        os.mkdir(handlers_dir)

        # Crear archivos __init__.py

        c_init = open(f'{handlers_dir}__init__.py','w')
        c_init.close()

        # Leer los pre-code

        db_code = open(f'{HERE}/db.py','r')
        db_code = db_code.read()

        main_code = open(f'{HERE}/ptbot/main.py','r')
        main_code = main_code.read()

        commands_code = open(f'{HERE}/ptbot/commands.py','r')   
        commands_code = commands_code.read()
                  
        # Escribir el pre-código

        file_main = open(f'{bot_dir}main.py','w')
        file_main.write(main_code.replace('token', token))
        file_main.close()
        
        file_db = open(f'{bot_dir}db.py','w')
        file_db.write(db_code)
        file_db.close()
                
        file_commands = open(f'{handlers_dir}commands.py','w')
        file_commands.write(commands_code)
        file_commands.close() 

        file_messages = open(f'{handlers_dir}messages.py','w')
        file_messages.write('from db import conn_lite3\n# Aqui creas las funciones para el MessageHandler')
        file_messages.close()

        file_messages = open(f'{handlers_dir}callbackquerys.py','w')
        file_messages.write('from db import conn_lite3\n# Aqui creas las funciones para el CallbackQueryHandler')
        file_messages.close()

        print(f'Proyecto creado con python-telegram-bot.')

def pyrobot ():
    
    bot_name = input('Entre el nombre de su bot de telegram: ')
    if bot_name == '':
        bot_name = 'pyrobot'

    token = input('Entre el token del bot : ')
    if token == '':
        token = 'TOKEN'  
    
    api_id = input('Entre su api_id: ')
    if api_id == '':
        api_id = 123456789

    api_hash = input('Entre su api_hash: ')   
    if api_hash == '':
        api_hash='abcdef123456'


    HERE = pathlib.Path(__file__).parent
    
    bot_dir = f'{bot_name}/'
    handlers_dir = f'{bot_dir}MyHandlers/'

    if os.path.exists(bot_dir):
        
        print(f'Ya exite un proyecto llamado {bot_name}')
    
    else :

        # Crear carpetas para el nuevo proyecto
 
        os.mkdir(bot_name)
        os.mkdir(handlers_dir)

        # Crear archivos __init__.py

        c_init = open(f'{handlers_dir}__init__.py','w')
        c_init.close()

        # Leer los pre-code

        db_code = open(f'{HERE}/db.py','r')
        db_code = db_code.read()

        main_code = open(f'{HERE}/pyrobot/main.py','r')
        main_code = main_code.read()

        commands_code = open(f'{HERE}/pyrobot/commands.py','r')   
        commands_code = commands_code.read()
        
        callback_code = open(f'{HERE}/pyrobot/callbackquerys.py','r')   
        callback_code = callback_code.read()
        
        
        # Escribir el pre-código

        file_main = open(f'{bot_dir}main.py','w')
        file_main.write(main_code.replace('TOKEN', token).replace('my_pyrobot',bot_name).replace('apiid',api_id).replace('apihash',api_hash))
        file_main.close()    

        file_db = open(f'{bot_dir}db.py','w')
        file_db.write(db_code)
        file_db.close()
                
        file_commands = open(f'{handlers_dir}commands.py','w')
        file_commands.write(commands_code)
        file_commands.close() 

        file_messages = open(f'{handlers_dir}messages.py','w')
        file_messages.write('from db import conn_lite3\n# Archivo para el MessageHandler')
        file_messages.close()

        file_messages = open(f'{handlers_dir}callbackquerys.py','w')
        file_messages.write(callback_code)
        file_messages.close()

        print(f'Proyecto creado con pyrogram.')

if __name__ == "__main__":
    pyrobot()


