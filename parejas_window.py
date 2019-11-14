import sys
#from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow,QTableWidget, QTableWidgetItem,QPushButton,QMessageBox
from PyQt5.uic import loadUi
from procesos import crea_triggers
from sorteo import *
from mesas_parejas1 import mesa_pareja1
import sqlite3



class Incripcion_parejas(QMainWindow):
    def __init__(self):
        super(Incripcion_parejas,self).__init__()
        loadUi('parejas_window.ui',self)
        crea_triggers()
        # boton de guardar parejas
        self.guarda_pareja.clicked.connect(self.nueva_pareja)
        # boton de borrar parejas
        self.borra_pareja.clicked.connect(self.borrar_pareja)
        self.cerrar_inscripcion.clicked.connect(self.cierre_i)
        self.sorteo.clicked.connect(self.sorteo_mesa_pareja)

    


    def cierre_i(self):
        mi_lista = sorteo()
        out = create_random_tables(mi_lista)
        crea_parejas_sorteo()
        
    def sorteo_mesa_pareja(self):
        mesa_pareja1()
        
    def run_query(self,query, parameters=()):
        with sqlite3.connect("BBDD_Domino") as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def lee_pareja(self):
        self.registros.clearContents()
        index=0
    # Leyendo data
        query = 'SELECT * FROM parejas ORDER BY id DESC'
        db_rows = self.run_query(query)
        for filas in db_rows:
            ids = filas[0] # ID
            Jugador1 = filas[1] # Jugador1
            Jugador2 = filas[2] # Jugador2
            Club = filas[3] # Club

            # Ahora organizamos los datos en la tabla creada anteriormente
            self.registros.setRowCount(index + 1)
            self.registros.setItem(index, 0, QTableWidgetItem(str(ids)))
            self.registros.setColumnWidth(0,50)
            self.registros.setItem(index, 1, QTableWidgetItem(Jugador1))
            self.registros.setColumnWidth(1,150)
            self.registros.setItem(index, 2, QTableWidgetItem(Jugador2))
            self.registros.setColumnWidth(2,150)
            self.registros.setItem(index, 3, QTableWidgetItem(Club))
            self.registros.setItem(index, 4,QTableWidgetItem(Jugador1+ " / "+ Jugador2))
            self.registros.setColumnWidth(4,300)

            index += 1

    def Validacion(self):
        if len(self.Entry_jugador1.text())==0 or len(self.Entry_Jugador2.text())==0 or len(self.Enry_Club.text())==0:
            vale="1"
        else:
            vale="2"
        return vale
    def nueva_pareja(self):
        vale=self.Validacion()
        if vale=="2":
            query = 'INSERT INTO Parejas VALUES(NULL, ?, ?, ?, ?)'
            parameters = (self.Entry_jugador1.text(),
                      self.Entry_Jugador2.text(), self.Enry_Club.text(), (self.Entry_jugador1.text() + " / " + self.Entry_Jugador2.text()))
                 
            self.run_query(query, parameters)
            #borrando campos de entrada
            self.Entry_jugador1.setText(" ")
            self.Entry_Jugador2.setText(" ")
            self.Enry_Club.setText(" ")
            
        else:
            QMessageBox.warning(self, "Error","Los campos de jugadores y club tienen que rellenarse")

            # mostrando data  
            
        self.lee_pareja()

    # ----borrar parejas
    def borrar_pareja(self):
        fila_seleccionada=self.registros.selectedItems()
        if fila_seleccionada:
            fila=fila_seleccionada[0].row()
            self.pareja_inscrita=fila_seleccionada[4].text()
            #self.registros.removeRow(fila)
        else:
            QMessageBox.warning(self,"Error","Tienes que seleccionar una fila")

        query = 'DELETE FROM Parejas WHERE pareja_inscrita = ? '
        self.run_query(query, (self.pareja_inscrita,))
        self.lee_pareja()

if __name__ == "__main__":
    app =  QApplication(sys.argv)
    window = Incripcion_parejas()
    window.show()
    sys.exit(app.exec_())
