import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.1.2' 
PACKAGE_NAME = 'RunTeleBot'  
AUTHOR = 'Raú Enrique Cobiellas Colomé' 
AUTHOR_EMAIL = 'raulcobiellas@gmail.com' 
URL = 'https://github.com/RaulCobiellas' 

LICENSE = 'MIT' 
DESCRIPTION = 'Librería para ayudar a crear bots de Telegram.' 
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8') 
LONG_DESC_TYPE = "text/markdown"


INSTALL_REQUIRES = [
      'python-telegram-bot',
      'pymysql',
      'pyrogram',
      'telethon'
      ]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)