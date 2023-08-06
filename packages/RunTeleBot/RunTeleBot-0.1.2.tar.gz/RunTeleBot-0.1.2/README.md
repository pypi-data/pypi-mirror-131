## RunTeleBot

RunTeleBot es una librería desarrollada para ayudar a crear bots en telegram usando diferentes librerías como `python-telegram-bot` y `pyrogram` 

### Como usar ?
- Creamos un archivo python llamado crear_bot.py (por ejemplo) en donde importaremos y ejecutaremos la función `ptbot()` o `pyrobot()` de la librería , cuando ejecutemos esto creará el esqueleto básico para cualquier bot en telegram (copia y pega el código de abajo en el archivo):

```python
# Crear bot con python-telegram-bot (ptb)
from RunTeleBot import ptbot
ptbot()
```

```python
# Crear bot con pyrogram
from RunTeleBot import pyrobot
pyrobot()
```

Una vez que ejecutemos el script nos pedirá ingresar algunos datos incluyendo
el token del bot (si no ingresamos ningún dato se creará el esqueleto del bot con los valores por defecto).

### [Chat de Telegram](https://t.me/RunCodeChat)
