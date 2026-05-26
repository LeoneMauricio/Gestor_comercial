import sqlite3

def conectar():
    conexion = sqlite3.connect("soderia.db")
    #conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion

def conectar_row():
    conexion = sqlite3.connect("soderia.db")
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion