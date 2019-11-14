import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
#from procesos import crea_triggers
#from parejas_window import Incripcion_parejas
import sqlite3

qtCreatorFile = "settings_window.ui" # Nombre del archivo aquí.

#Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
#------------ Creacion de la evntana en base al fichero ui----------------------
class Campeonato (QMainWindow):

    def __init__(self):
        super(Campeonato,self).__init__()
        loadUi('settings_window.ui',self)
        # ---------- creacion de los procesos de los botones-------------------
        self.boton_crea_bbdd.clicked.connect(self.crea_bbdd)
        self.boton_guardar.clicked.connect(self.nuevo_campeonato)
        

    

    #--------------- funcion de query en bases de datos------------------------
    def run_query(self,query, parameters=()):
        with sqlite3.connect("BBDD_Domino") as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    # ------------crea las bases de datos--------------------------------------
    def crea_bbdd(self):
        try:
            query=('''
                CREATE TABLE Settings(
                Nombre_Campeonato VARCHAR(50) PRIMARY KEY,
                Numero_partidas INTEGER,
                Grupo_A INTEGER,
                Puntos INTEGER,
                Partida_corte INTEGER)''')
            self.run_query(query)
            mensaje_st=("Las bases de datos han sido creadas con éxito")
            self.mensajes.setText(mensaje_st)
        except:
            mensaje_st="Las bases de datos ya existen"
            self.mensajes.setText(mensaje_st)

        query=('''
            CREATE TABLE IF NOT EXISTS Parejas(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            jugador1 VARCHAR(30) NOT NULL,
            jugador2 VARCHAR(30) NOT NULL,
            club VARCHAR(30) NOT NULL,
            pareja_inscrita VARCHAR(70))
                ''')
        self.run_query(query)

        query=('''
            CREATE TABLE IF NOT EXISTS Res_parejas(
            Id_pareja INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            Grupo VARCHAR(5) DEFAULT "A",
            Partida INTEGER,
            Mesa INTEGER,
            Ganada INTEGER,
            Npareja INTEGER,
            Nombre_pareja VARCHAR(65),
            Result_Partida INTEGER,
            Diferencia INTEGER)  
            ''')
        self.run_query(query)
        query = 'DROP TABLE IF EXISTS  primer_ranking'
        self.run_query(query)

    #try:
        query = ('''CREATE TABLE primer_ranking(
            NparejaN INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            Nombre_parejaN VARCHAR(75) NOT NULL,
            Mesa INTEGER)
             ''')
        self.run_query(query)

    def crea_triggers (self):
# Trigger  para Insertar parejas en la tabla resultados
        query = ('''CREATE TRIGGER IF NOT EXISTS pareja_ai
                AFTER INSERT 
                ON Parejas
                FOR EACH ROW
                    BEGIN
                        INSERT INTO Res_parejas (Npareja, Nombre_pareja)
                        VALUES (NEW.id, NEW.pareja_inscrita);
                    END''')
        self.run_query(query)

# Trigger  para Borrar parejas en la tabla resultados
        query = ('''CREATE TRIGGER IF NOT EXISTS pareja_bd
                BEFORE DELETE
                ON Parejas
                FOR EACH ROW
                    BEGIN
                        DELETE FROM Res_parejas WHERE Nombre_pareja==OLD.pareja_inscrita;
                    END''')
        self.run_query(query)
    #-------------------valores de los radio buttons-------------
    def valores_grupo(self):
        if self.grupoA.isChecked():
            valorg=1
        elif self.grupoayb.isChecked():
            valorg=2
        else:
            valorg=3
        return valorg

    def valores_tantos(self):
        if self.puntos.isChecked():
            valort=1
        elif self.puntos_total.isChecked():
            valort=2
        else:
            valort=3
        return valort 
    #---------------- entrada de datos del campeonato----------------
    def nuevo_campeonato(self):
        try:  
            nombre_c=self.n_campeonato.text()
            #print(nombre_c)
            numero_partidas=self.n_partidas.text()
            #print(numero_partidas)
            grupo=self.valores_grupo()
            #print(grupo)
            tantos=self.valores_tantos()
            #print(tantos)
            part_cort= self.partida_corte.text()
            #print(part_cort)
    
            if len(nombre_c)==0 or len(numero_partidas)==0 or grupo==3 or tantos==3:
                mensaje_st=("Se tienen que rellenar los campos")
                self.mensajes.setText(mensaje_st) 
            
            else:
                query=("INSERT INTO Settings VALUES (?,?,?,?,?)")

                parameters=(nombre_c,numero_partidas,grupo,tantos,part_cort)

                self.run_query(query,parameters)
                mensaje_st=("El Campeonato ha sido creado con éxito")
                self.mensajes.setText(mensaje_st)
        except:
            mensaje_st="Antes, tienes que Crear las Bases de Datos"
            self.mensajes.setText(mensaje_st)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Campeonato()
    window.show()
    sys.exit(app.exec_())

