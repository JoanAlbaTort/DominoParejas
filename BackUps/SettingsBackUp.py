from tkinter import *
from tkinter import messagebox
from crear_bbdd import conexion_Parejas, conexion_Resultados


import sqlite3
# --------------------------Funciones---------------------------------

# -------crea la base de datos ------------------


def conexion_BBDD_Domino():

    mi_conexion = sqlite3.connect("BBDD_Domino")
    mi_cursor = mi_conexion.cursor()
    try:
        mi_cursor.execute('''
            CREATE TABLE Settings(
            Nombre_Campeonato VARCHAR(50) PRIMARY KEY,
            Numero_partidas INTEGER,
            Grupo_A INTEGER,
            Puntos INTEGER,
            Partida_corte INTEGER,
            Pareja_corte INTEGER)''')
        messagebox.showinfo("BBDD", "BBDD creada con éxito")
    except:
        messagebox.showwarning("¡Atención!", "La BBDD ya existe")

# ---para salir de la pantalla de settings


def salir_parametros():
    valor = messagebox.askquestion("Salir", "¿Deseas salir de la ventana?")
    if valor == "yes":
        root.destroy()

# ----limpia los par ametros escritos dentro de Settings


def limpiar_parametros():
    nombre_campeonato.set("")
    numero_partidas.set(0)
    grupo_b.set(1)
    todos_puntos.set(2)
    b_partida.set(0)
    b_pareja.set(0)

# ----crea parametros de settings


def crear_parametros():
    mi_conexion = sqlite3.connect("BBDD_Domino")
    mi_cursor = mi_conexion.cursor()
    datos = nombre_campeonato.get(), numero_partidas.get(), grupo_b.get(
    ), todos_puntos.get(), b_partida.get(), b_pareja.get()
    mi_cursor.execute("INSERT INTO Settings VALUES (?,?,?,?,?,?)", (datos))

    mi_conexion.commit()
    messagebox.showinfo("BBDD", "Registro insertado con éxito")

# ---activa los campos de pareja y partida de corte en caso de grupo A y B


def activa_campos():
    if grupo_b.get() == 1:
        cuadro_b_pareja.config(state="disabled")
        cuadro_b_partida.config(state="disabled")
    else:
        cuadro_b_pareja.config(state="normal")
        cuadro_b_partida.config(state="normal")


# ----crea la vetana para introducir los parametros de Settings
root = Tk()
root.title("Settings")
barra = Menu()
root.config(menu=barra)
# ----------menu de la ventana--------
file = Menu(barra)
file.add_command(label="Crear BBDD", command=lambda: (conexion_BBDD_Domino(), conexion_Resultados(), conexion_Parejas()))
file.add_command(label="Hacer Grupo B")
file.add_separator()
file.add_command(label="Cerrar Parejas")
file.add_command(label="Hacer Sorteo")
file.add_command(label="Cerrar partidas")
file.add_command(label="Crear Mesas/Parejas")
file.add_separator()
file.add_command(label="Salir")

edit = Menu(barra)
edit.add_command(label="Parametros")
edit.add_command(label="Parejas")
edit.add_command(label="Resultados")


info = Menu(barra)
info.add_command(label="Listado Parejas")
info.add_command(label="Listado Mesas/Parejas")
info.add_command(label="Listado Posicion Parejas")

mhelp = Menu(barra)
mhelp.add_command(label="Licencia")
mhelp.add_command(label="Acerca de...", )

barra.add_cascade(label="General", menu=file)

barra.add_cascade(label="Datos", menu=edit)

barra.add_cascade(label="Información", menu=info)

barra.add_cascade(label="Ayuda", menu=mhelp)

frame1 = Frame(root)
frame1.pack()
frame2 = Frame(root)
frame2.pack()
# ------------- aqui las variables

nombre_campeonato = StringVar()
numero_partidas = IntVar()
b_partida = IntVar()
b_pareja = IntVar()
var = IntVar()
grupo_b = IntVar()
todos_puntos = IntVar()

# -------------aqui los campos---------------
cuadro_campeonato = Entry(frame1, textvariable=nombre_campeonato)
cuadro_campeonato.focus()
cuadro_campeonato.grid(row=0, column=1, padx=10, pady=10)
cuadro_campeonato.config(justify="right")

cuadro_numero_partidas = Entry(frame1, textvariable=numero_partidas, width=3)
cuadro_numero_partidas.grid(row=0, column=3, padx=10, pady=10)
cuadro_numero_partidas.config(justify="right")

cuadro_b_partida = Entry(frame2, textvariable=b_partida, width=3)
cuadro_b_partida.grid(row=0, column=4, padx=10, pady=10)
cuadro_b_partida.config(justify="right")

cuadro_b_pareja = Entry(frame2, textvariable=b_pareja, width=3)
cuadro_b_pareja.grid(row=1, column=4, padx=10, pady=10)
cuadro_b_pareja.config(justify="right")

# --------------------------aqui radio buttons-------------------

radio_grupo_a = Radiobutton(frame2, text="Grupo A", variable=grupo_b, value=1, command=activa_campos)
radio_grupo_a.grid(row=0, column=1, padx=10, pady=10)
radio_grupo_a.invoke()

radio_grupo_b = Radiobutton(frame2, text="Grupo A y B", variable=grupo_b, value=2, command=activa_campos)
radio_grupo_b.grid(row=1, column=1, padx=10, pady=10)

radio_total = Radiobutton(frame2, text="Todos los puntos", variable=todos_puntos,  value=2)
radio_total.grid(row=1, column=0, padx=10, pady=10)

radio_300 = Radiobutton(frame2, text="300 puntos", variable=todos_puntos, value=1)
radio_300.grid(row=0, column=0, padx=10, pady=10)
radio_300.invoke()


# ------------aqui las etiquetas------------

campeonato_label = Label(frame1, text="Nombre Campeonato ")
campeonato_label.grid(row=0, column=0, sticky="e", padx=10, pady=10)

numero_partidas_label = Label(frame1, text="Número Partidas ")
numero_partidas_label.grid(row=0, column=2, sticky="e", padx=10, pady=10)

b_partida_label = Label(frame2, text="Partida de Corte ")
b_partida_label.grid(row=0, column=2, sticky="e", padx=10, pady=10)

b_pareja_label = Label(frame2, text="P. Pareja de corte ")
b_pareja_label.grid(row=1, column=2, sticky="e", padx=10, pady=10)

# ---------------------------aqui los botones--------------------------------------

mi_frame3 = Frame(root)
mi_frame3.pack()

boton_crear = Button(mi_frame3, text="Crear",command=crear_parametros, anchor=CENTER)
boton_crear.grid(row=1, column=0,  sticky=W + E, padx=10, pady=10)

boton_limpiar = Button(mi_frame3, text="Limpiar Campos",command=limpiar_parametros, anchor=CENTER)
boton_limpiar.grid(row=1, column=1, sticky=W + E, padx=10, pady=10)

boton_Salir = Button(mi_frame3, text="Salir de la ventana",command=salir_parametros, anchor=CENTER)
boton_Salir.grid(row=1, column=3, sticky=W + E, padx=10, pady=10)

boton_bbdd = Button(mi_frame3, text="Crear BBDD",command=lambda: (conexion_BBDD_Domino(), conexion_Resultados(), conexion_Parejas()), anchor=CENTER)
boton_bbdd.grid(row=1, column=4, sticky=W + E, padx=10, pady=10)

root.mainloop()
