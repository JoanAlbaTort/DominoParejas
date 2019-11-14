import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QTableWidgetItem,QMessageBox,QPushButton
from PyQt5.uic import loadUi
import sqlite3

class Asignacion_mesas(QMainWindow):
    def __init__(self):
        super(Asignacion_mesas,self).__init__()
        loadUi('mesas_a_jugar.ui',self)

        query=" SELECT MAX(Partida) FROM Res_parejas"  
        num_partida_actual=self.run_query(query)  
        for primer in num_partida_actual:
            la_part=primer[0]
            
        if la_part<=1:
            self.lee_mesas_sorteo()
        else:
            self.lee_mesas_partida_nueva()
    def run_query(self,query, parameters=()):
        with sqlite3.connect("BBDD_Domino") as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def lee_mesas_sorteo(self):
        self.tableWidget.clearContents()
        index=0
    # Leyendo data
        query = 'SELECT Id,Nombre_parejaN, Mesa FROM Parejas INNER JOIN primer_ranking ON pareja_inscrita=Nombre_parejaN ORDER BY Id ASC'
        db_ranking = self.run_query(query)
        for pr in db_ranking:
            #Id=s[0]
            n_pareja= pr[0] # Numero Pareja
            nombre_pareja = pr[1] # Nombre Pareja
            mesa_asignada = pr[2] # Mesa
            
         
        # Ahora organizamos los datos en la tabla creada anteriormente
            self.tableWidget.setRowCount(index + 1)
            self.tableWidget.setItem(index, 0, QTableWidgetItem(str(n_pareja)))
            self.tableWidget.setColumnWidth(0,50)
            self.tableWidget.setItem(index, 1, QTableWidgetItem(nombre_pareja))
            self.tableWidget.setColumnWidth(1,300)
            self.tableWidget.setItem(index, 2, QTableWidgetItem(str(mesa_asignada)))
            self.tableWidget.setColumnWidth(2,50)
            
            index += 1  
    def lee_mesas_partida_nueva(self):
        self.tableWidget.clearContents()
        index=0
    # Leyendo data
        query = 'SELECT Id,Nombre_parejaN, Mesa FROM Parejas INNER JOIN Mesa_partida ON pareja_inscrita=Nombre_parejaN ORDER BY Mesa ASC'
        db_ranking = self.run_query(query)
        for pr in db_ranking:
            #Id=s[0]
            n_pareja= pr[0] # Numero Pareja
            nombre_pareja = pr[1] # Nombre Pareja
            mesa_asignada = pr[2] # Mesa
            
         
        # Ahora organizamos los datos en la tabla creada anteriormente
            self.tableWidget.setRowCount(index + 1)
            self.tableWidget.setItem(index, 0, QTableWidgetItem(str(n_pareja)))
            self.tableWidget.setColumnWidth(0,50)
            self.tableWidget.setItem(index, 1, QTableWidgetItem(nombre_pareja))
            self.tableWidget.setColumnWidth(1,300)
            self.tableWidget.setItem(index, 2, QTableWidgetItem(str(mesa_asignada)))
            self.tableWidget.setColumnWidth(2,50)
            
            index += 1
if __name__ == "__main__":
    app =  QApplication(sys.argv)
    window = Asignacion_mesas()
    window.show()
    sys.exit(app.exec_())
       
