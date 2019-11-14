from tkinter import messagebox

from procesos import*
import sqlite3


def orden_sorteo():
    lista_mesa = []
    query = 'SELECT NparejaN FROM primer_ranking '
    parejas = run_query(query)
    for i in parejas:
        np = i[0]
        mesa = round((np/2)+0.1)
        lista_mesa.append(mesa)
    return (lista_mesa)

    # print(lista_mesa)


def orden_inscripcion():
    lista_orden = []
    query = 'SELECT NparejaN FROM primer_ranking '
    parejas = run_query(query)
    for i in parejas:
        np = i[0]
        lista_orden.append(np)
    return (lista_orden)


def mesa_pareja1():
    lista_mesa = orden_sorteo()
    lista_orden = orden_inscripcion()
    proba = zip(lista_mesa, lista_orden)
    for h in proba:
        a = str(h[0])
        b = str(h[1])

        #print(a, b)

        query = "UPDATE primer_ranking SET Mesa=(?) WHERE NparejaN=(?) "
        parameters = (a, b)
    # print(lista_mesa)
        run_query(query, parameters,)


mesa_pareja1()
messagebox.showinfo("MESAS PAREJAS", "La primera partida está preparada")
# print(lista_mesa)
# print(lista_orden)
