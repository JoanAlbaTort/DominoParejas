
from procesos import*
import sqlite3


def Mesa_orden():
    part=numero_partida()
    lista_mesa = []
    query = 'SELECT Id_par FROM Mesa_partida WHERE PartidaN =(?) '
    parameters=(str(part))
    parejas = run_query(query,parameters)
    for i in parejas:
        np = i[0]
        mesa = round((np/2)+0.1)
        lista_mesa.append(mesa)
    return (lista_mesa)

    # print(lista_mesa)


def Ranking():
    part=numero_partida()
    lista_orden = []
    query = 'SELECT Id_par FROM Mesa_partida WHERE PartidaN=(?) '
    parameters=(str(part))
    parejas = run_query(query,parameters)
    for i in parejas:
        np = i[0]
        lista_orden.append(np)
    return (lista_orden)
    
def numero_partida():
    query="SELECT MAX(PartidaN) FROM Mesa_partida"
    n_part =run_query(query)
    for partida_jugando in n_part:
        part=partida_jugando[0]
        return part

def mesa_pareja():
    lista_mesa = Mesa_orden()
    lista_orden = Ranking()
    part=numero_partida()
    proba = zip(lista_mesa, lista_orden)
    for h in proba:
        a = str(h[0])
        b = str(h[1])
        #print(a, b)
        query = "UPDATE Mesa_partida SET Mesa=(?) WHERE Id_par=(?) "
        parameters = (a, b)
        #print(lista_mesa)
        run_query(query, parameters,)
    query="SELECT id,Mesa,pareja_inscrita FROM Parejas INNER JOIN Mesa_partida ON pareja_inscrita=Nombre_parejaN"
    distribucion_mesas=run_query(query)

    lista_m=[]
    lista_p=[]
    for mesas in distribucion_mesas:
        n=mesas[0]
        m=mesas[1]
        p=mesas[2]
        lista_m.append(m)
        lista_p.append(p)
        #print( "La pareja " +str(n) + " "+p+" en la mesa " + str(m))
    l_m_p=zip(lista_m,lista_p)
    for r in l_m_p:
        mes=str(r[0])
        par=r[1]
        query="UPDATE Res_parejas SET Mesa=(?) WHERE Nombre_pareja=(?) AND Partida=(?)"
        parameters=(mes,par,part)
        run_query(query,parameters)

    # creacion de las mesas en partidas        
    """query=" SELECT Numero_partidas FROM Settings"
    npartidas=run_query(query)
    for max_p in npartidas:
        p=max_p[0]
        partida=part
    if partida<=p:
        mesa_pareja()"""
    
