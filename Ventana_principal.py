import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow,QMessageBox
from PyQt5.uic import loadUi
from settings_window import Campeonato
from parejas_window import Incripcion_parejas
from resultados_window import Resultados_partidas
from ranking import clasificacion
from Mesas_a_jugar import Asignacion_mesas
import sqlite3


class VentanaPrincipal(QMainWindow):

    def __init__(self):
        super(VentanaPrincipal, self).__init__()
        loadUi('ventana_inicial.ui', self)
        self.crea_campeonato.clicked.connect(self.abrir_v_settings)
        self.Inscribe_parejas.clicked.connect(self.abrir_v_parejas)
        self.resultados.clicked.connect(self.abrir_v_resultados)
        self.ver_mesas.clicked.connect(self.abrir_v_ver_mesas)
        self.ver_ranking.clicked.connect(self.abrir_v_ranking)
    def abrir_v_settings(self):
        self.otraventana=Campeonato()
        self.otraventana.show()
    def abrir_v_parejas(self):
        self.otraventava=Incripcion_parejas()
        self.otraventava.show() 
    
    def abrir_v_resultados(self):
        self.otraventava=Resultados_partidas()
        self.otraventava.show() 
    
    
    def abrir_v_ver_mesas(self):
    
        self.otraventava=Asignacion_mesas()
        self.otraventava.show()
    def abrir_v_ranking(self):
    
        self.otraventava=clasificacion()
        self.otraventava.show()     
    

app = QApplication(sys.argv)
main = VentanaPrincipal()
main.show()
sys.exit(app.exec_())