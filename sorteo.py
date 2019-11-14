from PyQt5.QtWidgets import QApplication, QMainWindow,QTableWidget, QTableWidgetItem,QPushButton,QMessageBox
from PyQt5.uic import loadUi
from procesos import run_query,crea_triggers
from mesas_parejas1 import mesa_pareja1
import random
import sqlite3




def crea_parejas_sorteo():
    query = 'DROP TABLE IF EXISTS  primer_ranking'
    run_query(query)

    #try:
    query = ('''CREATE TABLE primer_ranking(
            NparejaN INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            Nombre_parejaN VARCHAR(75) NOT NULL,
            Mesa INTEGER)
             ''')
    run_query(query)

        # ----numerar las parejas correlativamente despues del sorteo
     
    for i in out:
        Nombre_parejaN = i
        query = 'INSERT INTO primer_ranking (Nombre_parejaN) VALUES (?)'
        parameters = (Nombre_parejaN)
        run_query(query, parameters)
        #QMessageBox.critical (self,"TABLA DE SORTEO", "La tabla de sorteo se ha realizado con exito, ahora ejecute la opción de creación de primera mesa")
    #except:
        #QMessageBox.critical (self,"¡Atención!", "La tabla del sorteo ya ha sido creada")
# ----crea la lista del sorteo

def sorteo():
    mi_lista = []
    query = 'SELECT Nombre_pareja FROM Res_parejas'
    lista_inscritos = run_query(query,)
    for p in lista_inscritos:
        inscritos = (p)
        mi_lista.append(inscritos)
    return mi_lista

# ----hace el sorteo--------
def create_random_tables(input_list):
    random_list = random.sample(range(len(mi_lista)), len(mi_lista))
    out_list = []
    for i in random_list:
        my_select = mi_lista[i]
        out_list.append(my_select)
    return out_list

# ---- ejecutar Sorteo
   
mi_lista = sorteo()
out = create_random_tables(mi_lista)
#print(out)
#crea_parejas_sorteo()



