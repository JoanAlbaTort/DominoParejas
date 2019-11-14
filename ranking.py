import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QTableWidgetItem,QMessageBox,QPushButton
from PyQt5.uic import loadUi
import sqlite3

class clasificacion(QMainWindow):
    def __init__(self):
        super(clasificacion,self).__init__()
        loadUi('ranking.ui',self)
        self.lee_ranking()
        
    def run_query(self,query, parameters=()):
        with sqlite3.connect("BBDD_Domino") as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def lee_ranking(self):
        self.tableWidget.clearContents()
        index=0
    # Leyendo data
        query = 'SELECT Id_pareja,Grupo,SUM(Ganada) AS PG,SUM(Diferencia) AS Puntos, MAX(Partida) AS PJ , Nombre_pareja, Mesa,Result_Partida FROM Res_parejas GROUP BY Nombre_pareja ORDER BY Grupo ASC,SUM(Ganada)DESC, SUM(Diferencia) DESC'
        db_ranking = self.run_query(query)
        for s in db_ranking:
            #Id=s[0]
            grupo= s[1] # Grupo
            pg = s[2] # partidas Ganadas
            puntos = s[3] # Puntos
            partida = s[4] # Partida
            pareja = s[5] # Pareja
            mesa = s[6] # mesa
            reultado=s[7] # resultado
         
        # Ahora organizamos los datos en la tabla creada anteriormente
            self.tableWidget.setRowCount(index + 1)
            #self.tableWidget.setItem(index, 0, QTableWidgetItem(str(Id)))
            self.tableWidget.setItem(index, 0, QTableWidgetItem(grupo))
            self.tableWidget.setColumnWidth(0,50)
            self.tableWidget.setItem(index, 1, QTableWidgetItem(str(pg)))
            self.tableWidget.setColumnWidth(1,50)
            self.tableWidget.setItem(index, 2, QTableWidgetItem(str(puntos)))
            self.tableWidget.setColumnWidth(2,75)
            self.tableWidget.setItem(index, 3, QTableWidgetItem(pareja))
            self.tableWidget.setColumnWidth(3,300)
            self.tableWidget.setItem(index, 4, QTableWidgetItem(str(partida)))
            self.tableWidget.setColumnWidth(3,300)
            self.tableWidget.setItem(index, 5, QTableWidgetItem(str(mesa)))
            self.tableWidget.setItem(index, 6, QTableWidgetItem(str(reultado)))
            index += 1  
   
if __name__ == "__main__":
    app =  QApplication(sys.argv)
    window = clasificacion()
    window.show()
    sys.exit(app.exec_())
       
