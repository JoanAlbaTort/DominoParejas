import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QTableWidgetItem,QMessageBox,QPushButton
from PyQt5.uic import loadUi
from nueva_partida import *
from mesas_parejas_resto import mesa_pareja
import sqlite3


class Resultados_partidas(QMainWindow):
    def __init__(self):
        super(Resultados_partidas,self).__init__()
        loadUi('resultados_window.ui',self)
        self.leer_mesa.clicked.connect(self.decir_mesa)
        self.lee_resultado_mesa()
        self.npart.setText(str(self.saber_juego()))
        self.boton_new_res.clicked.connect(self.nuevo_resultado)
        self.boton_calcula.clicked.connect(self.lee_calculos)
        self.boton_nuevap.clicked.connect(self.nova_partida)

    def nova_partida(self): 
        crea_Mesa_pareja()
        mesa_pareja()

    #--------------- funcion de query en bases de datos------------------------
    def run_query(self,query, parameters=()):
        with sqlite3.connect("BBDD_Domino") as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters,)
            conn.commit()
        return result

    def saber_juego(self):
        query="SELECT MAX(Partida) FROM Res_parejas"
        n_part =self.run_query(query)
        for partida_jugando in n_part:
            part=partida_jugando[0]
            return part

    def decir_mesa(self):
        if self.nmesa.text()!=0:
            query="SELECT Nombre_pareja FROM Res_parejas WHERE Partida=(?) AND Mesa=(?)"
            parameters=(self.npart.text(),self.nmesa.text())
            nmes=self.run_query(query,parameters)
            listap=[]
            for mes in nmes:
                npareja=mes[0]
                listap.append(npareja)
            if len(listap)>1:
                jug1=listap[0]
                jug2=listap[1]
            else:
                jug1=listap[0]
                jug2=" "
        
        self.pareja_1.setText(jug1)
        self.pareja_2.setText(jug2)
        self.parejas_jugando()

    def parejas_jugando(self):        
            #self.mjugando.
            num_part_act=self.saber_juego()
            query="SELECT MAX(Mesa) FROM Res_parejas WHERE Partida=(?)"
            parameters=str(num_part_act)
            npc=self.run_query(query,parameters)
            for npart in npc:
                npt=npart[0]
                #print(npt)
            query="SELECT COUNT(Result_Partida) FROM Res_parejas WHERE Partida=(?) AND Result_Partida>0 "
            parameters=(self.npart.text())
            nmesas_jugando=self.run_query(query,parameters)
            for n in nmesas_jugando:
                nm=n[0]
                part_jugando =npt-(round((nm/2)+0.1))
                #print(nm)
            self.mjugando.setText(str(part_jugando))

    def lee_resultado_mesa(self):
        self.tabla_resultados.clearContents()
        
        index=0
    # Leyendo data
        query = 'SELECT * FROM Res_parejas WHERE Partida == (SELECT MAX(Partida) FROM Res_parejas) ORDER BY Mesa ASC'
        db_rows = self.run_query(query)
        for filas in db_rows:
            ids = filas[0] # ID
            grupo= filas[1] # Grupo
            partida = filas[2] # partida
            mesa = filas[3] # Mesa
            partidas_ganadas = filas[4] # Ganadasa
            numero_pareja = filas[5] # Ganadasa
            pareja = filas[6] # Pareja
            resultado = filas[7] # Resultado
            puntos = filas[8] # Puntos
            
            

            # Ahora organizamos los datos en la tabla creada anteriormente
            self.tabla_resultados.setRowCount(index + 1)
            self.tabla_resultados.setItem(index, 0, QTableWidgetItem(str(ids)))
            self.tabla_resultados.setColumnWidth(0,50)
            self.tabla_resultados.setItem(index, 1, QTableWidgetItem(grupo))
            self.tabla_resultados.setColumnWidth(1,50)
            self.tabla_resultados.setItem(index, 2, QTableWidgetItem(str(partidas_ganadas)))
            self.tabla_resultados.setItem(index, 3, QTableWidgetItem(str(puntos)))
            self.tabla_resultados.setItem(index, 4, QTableWidgetItem(str(numero_pareja)))
            self.tabla_resultados.setColumnWidth(4,50)
            self.tabla_resultados.setItem(index, 5, QTableWidgetItem(pareja))
            self.tabla_resultados.setColumnWidth(5,300)
            self.tabla_resultados.setItem(index, 6, QTableWidgetItem(str(resultado)))
            self.tabla_resultados.setItem(index, 7, QTableWidgetItem(str(partida)))
            self.tabla_resultados.setItem(index, 8, QTableWidgetItem(str(mesa)))
            index += 1

    def Validacion_res(self):
        if len(self.nmesa.text())==0 or len(self.pp1.text())==0 or len(self.pp2.text())==0:
            val="1"
        else:
            val="2"
        return val

    def lee_calculos(self):
        val=self.Validacion_res()
        if val=="2":
            self.pp1.text()
            self.pp2.text()
            self.dp1.setText(str(int(self.pp1.text())-int(self.pp2.text())))
            self.dp2.setText(str(int(self.pp2.text())-int(self.pp1.text())))
            if self.pp1.text()>self.pp2.text():
                self.ganada1.setText("1")
                self.ganada2.setText("0")
            else:
                self.ganada1.setText("0")
                self.ganada2.setText("1")
            

    def nuevo_resultado(self):
        val=self.Validacion_res()
        if val=="2":
            
            query = 'UPDATE Res_parejas SET Result_Partida=(?), Diferencia=(?), Ganada=(?)  WHERE Partida=(?) AND Mesa=(?) AND Nombre_pareja=(?)'
            parameters = (self.pp1.text(), self.dp1.text(),self.ganada1.text(),self.npart.text(),self.nmesa.text(),self.pareja_1.text())
            self.run_query(query, parameters,)
            query = 'UPDATE Res_parejas SET Result_Partida=(?), Diferencia=(?), Ganada=(?)  WHERE Partida=(?) AND Mesa=(?) AND Nombre_pareja=(?)'
            parameters = (self.pp2.text(), self.dp2.text(),self.ganada2.text(),self.npart.text(),self.nmesa.text(),self.pareja_2.text())
            self.run_query(query, parameters,)
           
            
        else:
            QMessageBox.warning(self, "Error","Los campos de jugadores y club tienen que rellenarse")
        
            # mostrando data  
          
        self.lee_resultado_mesa()   
        self.parejas_jugando()
           #borrando campos de entrada
        self.nmesa.setText(" ")
        self.pareja_1.setText(" ")
        self.pareja_2.setText(" ")
        self.pp1.setText(" ")
        self.pp2.setText(" ")
        self.dp1.setText(" ")
        self.dp2.setText(" ")
        self.ganada1.setText(" ")
        self.ganada2.setText(" ")    
        self.mjugando.setText(" ")
        
if __name__ == "__main__":
    app =  QApplication(sys.argv)
    window = Resultados_partidas()
    window.show()
    sys.exit(app.exec_())
 
 