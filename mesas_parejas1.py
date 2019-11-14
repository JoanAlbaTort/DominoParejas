
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
    query=" SELECT MAX(Partida) FROM Res_parejas"  
    numero_partida_actual=run_query(query)  
    for primera in numero_partida_actual:
        la_partida=primera[0]
        
    if la_partida==None: 
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
        query="SELECT id,Mesa,pareja_inscrita FROM Parejas INNER JOIN primer_ranking ON pareja_inscrita=Nombre_parejaN"
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
            query="UPDATE Res_parejas SET Mesa=(?) WHERE Nombre_pareja=(?)"
            parameters=(mes,par)
            run_query(query,parameters)
       
            query="UPDATE Res_parejas SET Partida = 1"
            run_query(query,)

    # creacion de las mesas en partidas       
query=" SELECT Numero_partidas FROM Settings"
npartidas=run_query(query,)

for max_partidas in npartidas:
    p=max_partidas[0]
partida=1
while partida<=p:
    if partida==1:
        mesa_pareja1()
    #else:
    partida+=1
pass
# QMessageBox.warning("MESAS PAREJAS", "La primera partida está preparada")
#print(lista_mesa)
#print(lista_orden)
