from tkinter import ttk
from tkinter import *
from crear_bbdd import *
from procesos import *
import sqlite3


# Lee Res_parejas de DDBB
def lee_resultado():
    # Limpiando Tabla
    registro = tree.get_children()
    for elemento in registro:
        tree.delete(elemento)
    # Leyendo data

    query = 'SELECT * FROM Res_parejas ORDER BY id_pareja DESC'
    db_rows = run_query(query)
    filas = db_rows.fetchall()

    # mostrando data
    for row in filas:
        tree.insert('', 0, text=row[0], values=(
            row[1], row[2], row[3]))

# Validacion de entrada usuario


def validation():
    return len(judagor1.get()) != 0 and len(judagor2.get()) != 0 and len(club.get()) != 0

# Creacion de una nueva pareja


def nueva_pareja():
    if validation():
        query = 'INSERT INTO Parejas VALUES(NULL, ?, ?, ?, ?)'
        parameters = (judagor1.get(),judagor2.get(), club.get(), (judagor1.get() + " / " + judagor2.get()))
        run_query(query, parameters)
        mensaje['text'] = 'El resultado de la mesa {} se ha aadido con éxito'.format((judagor1.get() + "/" + judagor2.get()))
        judagor1.delete(0, END)
        judagor2.delete(0, END)
        club.delete(0, END)
    else:
        mensaje['text'] = 'La partida y la mesa son necesarios'
    lee_resultado()

# ----borrar parejas


def borra_pareja():
    mensaje['text'] = ''
    try:
        # print(tree.item(tree.selection())['values'][0])
        tree.item(tree.selection())['values'][0]
    except IndexError as e:
        mensaje['text'] = 'Por favor selecciona un registro'
        return
    mensaje['text'] = ''
    jugador1 = tree.item(tree.selection())['values'][0]
    jugador2 = tree.item(tree.selection())['values'][1]
    pareja_inscrita = (str(jugador1) + " / "+str(jugador2))
    query = 'DELETE FROM Parejas WHERE pareja_inscrita = ? '
    run_query(query, (pareja_inscrita,))
    mensaje['text'] = 'El resultado de la mesa {} ha sido borrada con éxito'.format(pareja_inscrita)
    lee_resultado()

# ---edita parejas


def edita_pareja():
    mensaje['text'] = ''
    try:
        tree.item(tree.selection())['values'][0]
    except IndexError as e:
        mensaje['text'] = 'Por favor selecciona la pareja a editar'
        return
    jugador1 = tree.item(tree.selection())['values'][0]
    jugador2 = tree.item(tree.selection())['values'][1]
    club = tree.item(tree.selection())['values'][2]
    edit_wind = Toplevel()
    edit_wind.title = 'Editar pareja'
    # Jugador 1 a editar
    Label(edit_wind, text='Jugador1 a editar:').grid(row=0, column=1)
    Entry(edit_wind, textvariable=StringVar(edit_wind,value=jugador1),  fg='red', state='readonly').grid(row=0, column=2)
    # Nuevo jugador 1
    Label(edit_wind, text='Nuevo Jugador1:').grid(row=1, column=1)
    nuevo_jugador1 = Entry(edit_wind, textvariable=StringVar(edit_wind,value=jugador1))
    nuevo_jugador1.grid(row=1, column=2)

    # Jugador 2 a editar
    Label(edit_wind, text='Jugador2 a editar:').grid(row=2, column=1)
    Entry(edit_wind, textvariable=StringVar(edit_wind,value=jugador2), fg='red', state='readonly').grid(row=2, column=2)
    # Nuevo Jugador 2
    Label(edit_wind, text='Nuevo Jugador2:').grid(row=3, column=1)
    nuevo_jugador2 = Entry(edit_wind, textvariable=StringVar(edit_wind,value=jugador2))
    nuevo_jugador2.grid(row=3, column=2)

    # Club a editar
    Label(edit_wind, text='Club a editar:').grid(row=4, column=1)
    Entry(edit_wind, textvariable=StringVar(edit_wind,value=club), fg='red', state='readonly').grid(row=4, column=2)
    # Nuevo Club
    Label(edit_wind, text='Nuevo Club').grid(row=5, column=1)
    nuevo_club = Entry(edit_wind, textvariable=StringVar(edit_wind,value=club))
    nuevo_club.grid(row=5, column=2)

    Button(edit_wind, text='Actualizar', command=lambda: edita_registro(nuevo_jugador1.get(), jugador1, nuevo_jugador2.get(), jugador2, nuevo_club.get(), club)).grid(row=6, column=2, sticky=W)

    edit_wind.mainloop()

# ---edita el registro de edicion


def edita_registro(nuevo_jugador1, jugador1, nuevo_jugador2, jugador2, nuevo_club, club):
    pareja_inscrita = (str(jugador1) + " / "+str(jugador2))
    nueva_pareja_inscrita = (str(nuevo_jugador1) + " / "+str(nuevo_jugador2))
    query = 'UPDATE Parejas SET jugador1 = ?, jugador2 = ?, club=? WHERE jugador1 = ?AND jugador2 = ? AND club=?'
    parameters = (nuevo_jugador1, nuevo_jugador2, nuevo_club,jugador1, jugador2, club)
    run_query(query, parameters)
    # ---edita la pareja inscrita en Parejas
    query = 'UPDATE Parejas SET pareja_inscrita=? WHERE pareja_inscrita=?'
    parameters = (nueva_pareja_inscrita, pareja_inscrita)
    run_query(query, parameters)
    # ---edita Nombre_pareja en Res_parejas
    query = ' UPDATE Res_parejas SET Nombre_pareja= ? WHERE Nombre_pareja =?'
    parameters = (nueva_pareja_inscrita, pareja_inscrita)
    run_query(query, parameters)
    # edit_wind.destroy()
    mensaje['text'] = 'La pareja {} ha sido actualizada con éxito'.format(nueva_pareja_inscrita)
    lee_resultado()

# --iniciadores

window = Tk()
window.title("Resultado Partidas")
wind = window

# --creando frame container
frame = LabelFrame(wind, text='Resultados de las partidas')
frame.grid(row=0, column=0, columnspan=3, pady=20)
# --Partida 1 imput
Label(frame, text='Partida: ').grid(row=1, column=0,padx=5, pady=5)
judagor1 = Entry(frame, justify='right', fg='blue')
judagor1.grid(row=1, column=1,padx=5, pady=5)
# --Mesa 1 imput
Label(frame, text='Mesa: ').grid(row=1, column=3,padx=5, pady=5)
judagor1 = Entry(frame, justify='right', fg='blue')
judagor1.grid(row=1, column=4,padx=5, pady=5)

# --jugador 1 imput
Label(frame, text='Primera Pareja: ').grid(row=2, column=0,padx=5, pady=5)
judagor1 = Entry(frame, justify='right', fg='blue')
judagor1.grid(row=2, column=1,padx=5, pady=5)

# --jugador 2 imput
Label(frame, text='Segunda Pareja: ').grid(row=2, column=3,padx=5, pady=5)
judagor2 = Entry(frame, justify='right', fg='blue')
judagor2.grid(row=2, column=4, padx=5, pady=5)

# Puntos Pareja Primera Input
Label(frame, text='Puntos primera pareja: ').grid(row=3, column=0,padx=5, pady=5)
club = Entry(frame, justify='right', fg='blue')
club.grid(row=3, column=1,padx=5, pady=5)

# Puntos Pareja Segunda Input
Label(frame, text='Puntos segunda pareja: ').grid(row=3, column=3,padx=5, pady=5)
club = Entry(frame, justify='right', fg='blue')
club.grid(row=3, column=4,padx=5, pady=5)

# Diferencia Pareja Primera Input
Label(frame, text='Diferencia primera pareja: ').grid(row=4, column=0,padx=5, pady=5)
club = Entry(frame, justify='right', fg='blue')
club.grid(row=4, column=1,padx=5, pady=5)

# Diferencia Pareja Segunda Input
Label(frame, text='Diferencia segunda pareja: ').grid(row=4, column=3,padx=5, pady=5)
club = Entry(frame, justify='right', fg='blue')
club.grid(row=4, column=4,padx=5, pady=5)

radio_grupo_a = Radiobutton(frame, text="Ganadora pareja primera")
radio_grupo_a.grid(row=5, column=0, padx=10, pady=10)
radio_grupo_a.invoke()

radio_grupo_b = Radiobutton(frame, text="Ganadora pareja segunda")
radio_grupo_b.grid(row=5, column=3, padx=10, pady=10)

# Botón  nueva_pareja
ttk.Button(frame, text='Guardar Resultado', command=nueva_pareja).grid(row=6, columnspan=2, sticky=W + E)
# Mensaje  Salida
mensaje = Label(text='', fg='red')
mensaje.grid(row=6, column=0, columnspan=3, sticky=W + E)

# Tabla de pantalla
tree = ttk.Treeview(height=25, columns=["Jugador1", "Jugador2", "Club"])
tree.grid(row=6, column=0, columnspan=3)
tree.heading('#0', text='Numero Pareja', anchor=CENTER)
tree.heading('#1', text='Jugador1', anchor=CENTER)
tree.heading('#2', text='Jugador 2', anchor=CENTER)
tree.heading('#3', text='Club', anchor=CENTER)

# Botones Borrar Editar
ttk.Button(text='Borra Pareja', command=borra_pareja).grid(row=7, column=0, sticky=W + E)
ttk.Button(text='Edita Pareja', command=edita_pareja).grid(row=7, column=1, sticky=W + E)

# Llenando la tabla
lee_resultado()


window.mainloop()
