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

        main_code = open(f'{HERE}/main.py','r')
        main_code = main_code.read()

        commands_code = open(f'{HERE}/commands.py','r')   
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

        print(f'Proyecto {bot_name} creado.')


if __name__ == "__main__":
    ptbot()


