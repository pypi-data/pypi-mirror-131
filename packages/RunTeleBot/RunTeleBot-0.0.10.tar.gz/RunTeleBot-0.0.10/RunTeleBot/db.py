# Simplemente comentar o borrar la que no utilizarán

import sqlite3 # sqlite3
import pymysql # mysql
#import psycopg2 # postgresql


# Base de datos sqlite3
def conn_lite3 ():
    
    con = sqlite3.connect('database.sqlite3')
    cur = con.cursor()

    return con , cur

# Base de datos Mysql
def conn ():
    
    con = pymysql.connect(
        host='hostname',
        user='username',
        password='password',
        database='database')   
    cur = con.cursor()

    return con , cur

# Base de datos postgresql

# def conn_ps2 ():
    
#     con = psycopg2.connect(
#         database='database',
#         user='username', 
#         password='password',               
#         host='hostname',
#         port='5432')   
#     cur = con.cursor()

#     return con , cur