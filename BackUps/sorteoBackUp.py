from tkinter import messagebox
from procesos import*
import random
import sqlite3

# --creacion de una tabla intermedia


def crea_parejas_sorteo():
    try:
        query = ('''CREATE TABLE primer_ranking(
                    NparejaN INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    Nombre_parejaN VARCHAR(75) NOT NULL)
                    ''')
        run_query(query)

        # ----numerar las parejas correlativamente

        for i in out:
            Nombre_parejaN = i
            query = 'INSERT INTO primer_ranking (Nombre_parejaN) VALUES (?)'
            parameters = (Nombre_parejaN)
            run_query(query, parameters)
    except:
        messagebox.showwarning(
            "¡Atención!", "La tabla del sorteo ya ha sido creada")
# ----crea la lista del sorteo


def sorteo():
    mi_lista = []
    query = 'SELECT Nombre_pareja FROM Res_parejas'
    lista_inscritos = run_query(query)
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
crea_parejas_sorteo()
