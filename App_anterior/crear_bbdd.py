
import sqlite3

# --------------------------Funciones---------------------------------

def conexion_Parejas():

    mi_conexion = sqlite3.connect("BBDD_Domino")
    mi_cursor = mi_conexion.cursor()
    
    mi_cursor.execute('''
        CREATE TABLE IF NOT EXISTS Parejas(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        jugador1 VARCHAR(30) NOT NULL,
        jugador2 VARCHAR(30) NOT NULL,
        club VARCHAR(30) NOT NULL,
        pareja_inscrita VARCHAR(70))
        ''')
    



def conexion_Resultados():
    mi_conexion = sqlite3.connect("BBDD_Domino")
    mi_cursor = mi_conexion.cursor()
    
    mi_cursor.execute('''
        CREATE TABLE IF NOT EXISTS Res_parejas(
        Id_pareja INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        Grupo VARCHAR(5) DEFAULT "A",
        Partida INTEGER,
        Mesa INTEGER,
        Ranking INTEGER,
        Npareja INTEGER,
        Nombre_pareja VARCHAR(65),
        Res_propio INTEGER,
        Res_otro INTEGER,
        Diferencia INTEGER,            
        Ganada INTEGER)  
        ''')
   


"""def conexion_Mesa_partida():
    mi_conexion = sqlite3.connect("BBDD_Domino")
    mi_cursor = mi_conexion.cursor()
    
    mi_cursor.execute('''
            
        CREATE TABLE IF NOT EXISTS Mesa_partida(
        Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        Partida INTEGER NOT NULL,
        Mesa INTEGER NOT NULL,
        Npareja1 INTEGER NOT NULL,
        Npareja2 INTEGER NOT NULL)
        ''')"""
    
