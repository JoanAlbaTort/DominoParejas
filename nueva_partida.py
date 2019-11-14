from PyQt5.QtWidgets import QApplication, QMainWindow,QTableWidget, QTableWidgetItem,QPushButton,QMessageBox
from PyQt5.uic import loadUi
from procesos import *
import sqlite3




def crea_Mesa_pareja():

    query = 'DROP TABLE IF EXISTS Mesa_partida'
    run_query(query,)

    query = ('''CREATE TABLE Mesa_partida(
            Id_par INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            PartidaN INTEGER NOT NULL,
            Nombre_parejaN VARCHAR(75) NOT NULL,
            Mesa INTEGER)
             ''')
    run_query(query,)

    query = ('''CREATE TRIGGER IF NOT EXISTS mesa_ai
                    AFTER INSERT 
                    ON Mesa_partida
                    FOR EACH ROW
                        BEGIN
                            INSERT INTO Res_parejas (Npareja, Partida, Nombre_pareja)
                            VALUES (NEW.Id_par, NEW.PartidaN, NEW.Nombre_parejaN);
                            END''')
    partida=int(part)+1
    #parameters=(str(partida))
    run_query(query, )
    
        # ----numerar las parejas correlativamente despues de la partida
    for i in lista_m_p:
        Nombre_parejaN = i[0]
        print(Nombre_parejaN)
        query = 'INSERT INTO Mesa_partida (PartidaN,Nombre_parejaN) VALUES (?,?)'
        parameters = (partida,Nombre_parejaN)
        run_query(query, parameters,)
        
# ----crea la lista del orden
def saber_juego():
        query="SELECT MAX(Partida) FROM Res_parejas"
        n_part =run_query(query,)
        for partida_jugando in n_part:
            part=partida_jugando[0]
            if part==None:
                return 0
            else:
                return part
def orden():
    mi_lista = []
    query = 'SELECT Nombre_pareja FROM Res_parejas GROUP BY Nombre_pareja ORDER BY Grupo ASC, SUM (Ganada) DESC, SUM (Diferencia) DESC'
    lista_inscritos = run_query(query,) 
    for p in lista_inscritos:
        inscritos = p
        mi_lista.append(inscritos)
    return mi_lista


# ---- ejecutar 

part=saber_juego()
lista_m_p=orden()
#crea_Mesa_pareja()



