from tkinter import ttk
from tkinter import *
from crear_bbdd import *
from procesos import *
import sqlite3


# Lee Parejas de DDBB
def lee_pareja():
    # Limpiando Tabla
    records = tree.get_children()
    for element in records:
        tree.delete(element)
    # Leyendo data
    query = 'SELECT * FROM parejas ORDER BY id DESC'
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
        parameters = (judagor1.get(),
                      judagor2.get(), club.get(), (judagor1.get() + " / " + judagor2.get()))
        run_query(query, parameters)
        mensaje['text'] = 'La pareja {} se ha añadido con éxito'.format(
            (judagor1.get() + "/" + judagor2.get()))
        judagor1.delete(0, END)
        judagor2.delete(0, END)
        club.delete(0, END)
    else:
        mensaje['text'] = 'Los nombres de jugadores y club son necesarios'
    lee_pareja()

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
    mensaje['text'] = 'Pareja {} ha sido borrada con éxito'.format(
        pareja_inscrita)
    lee_pareja()

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
    Entry(edit_wind, textvariable=StringVar(edit_wind, value=jugador1),
          fg='red', state='readonly').grid(row=0, column=2)
    # Nuevo jugador 1
    Label(edit_wind, text='Nuevo Jugador1:').grid(row=1, column=1)
    nuevo_jugador1 = Entry(
        edit_wind, textvariable=StringVar(edit_wind, value=jugador1))
    nuevo_jugador1.grid(row=1, column=2)

    # Jugador 2 a editar
    Label(edit_wind, text='Jugador2 a editar:').grid(row=2, column=1)
    Entry(edit_wind, textvariable=StringVar(edit_wind, value=jugador2),
          fg='red', state='readonly').grid(row=2, column=2)
    # Nuevo Jugador 2
    Label(edit_wind, text='Nuevo Jugador2:').grid(row=3, column=1)
    nuevo_jugador2 = Entry(
        edit_wind, textvariable=StringVar(edit_wind, value=jugador2))
    nuevo_jugador2.grid(row=3, column=2)

    # Club a editar
    Label(edit_wind, text='Club a editar:').grid(row=4, column=1)
    Entry(edit_wind, textvariable=StringVar(edit_wind, value=club),
          fg='red', state='readonly').grid(row=4, column=2)
    # Nuevo Club
    Label(edit_wind, text='Nuevo Club').grid(row=5, column=1)
    nuevo_club = Entry(
        edit_wind, textvariable=StringVar(edit_wind, value=club))
    nuevo_club.grid(row=5, column=2)

    Button(edit_wind, text='Actualizar', command=lambda: edita_registro(nuevo_jugador1.get(
    ), jugador1, nuevo_jugador2.get(), jugador2, nuevo_club.get(), club)).grid(row=6, column=2, sticky=W)

    edit_wind.mainloop()

# ---edita el registro de edicion


def edita_registro(nuevo_jugador1, jugador1, nuevo_jugador2, jugador2, nuevo_club, club):
    pareja_inscrita = (str(jugador1) + " / "+str(jugador2))
    nueva_pareja_inscrita = (str(nuevo_jugador1) + " / "+str(nuevo_jugador2))
    query = 'UPDATE Parejas SET jugador1 = ?, jugador2 = ?, club=? WHERE jugador1 = ? AND jugador2 = ? AND club=?'
    parameters = (nuevo_jugador1, nuevo_jugador2,
                  nuevo_club, jugador1, jugador2, club)
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
    mensaje['text'] = 'La pareja {} ha sido actualizada con éxito'.format(
        nueva_pareja_inscrita)
    lee_pareja()


window = Tk()
window.title("Inscripción Parejas")
# --iniciadores
wind = window

# --creando frame container
frame = LabelFrame(wind, text='Añade nuevas parejas')
frame.grid(row=0, column=0, columnspan=3, pady=20)

# --jugador 1 imput
Label(frame, text='Primer Jugador: ').grid(row=1, column=0, padx=5, pady=5)
judagor1 = Entry(frame, justify='right', fg='blue')
judagor1.focus()
judagor1.grid(row=1, column=1, padx=5, pady=5)

# --jugador 2 imput
Label(frame, text='Segundo Jugador: ').grid(row=2, column=0, padx=5, pady=5)
judagor2 = Entry(frame, justify='right', fg='blue')
judagor2.grid(row=2, column=1, padx=5, pady=5)

# Club Input
Label(frame, text='Club: ').grid(row=3, column=0, padx=5, pady=5)
club = Entry(frame, justify='right', fg='blue')
club.grid(row=3, column=1, padx=5, pady=5)
# Botón  nueva_pareja
ttk.Button(frame, text='Guardar Pareja', command=nueva_pareja).grid(
    row=4, columnspan=2, sticky=W + E)
# Mensaje  Salida
mensaje = Label(text='', fg='red')
mensaje.grid(row=5, column=0, columnspan=3, sticky=W + E)

# Tabla de pantalla
tree = ttk.Treeview(height=30, columns=["Jugador1", "Jugador2", "Club"])
tree.grid(row=6, column=0, columnspan=3)
tree.heading('#0', text='Numero Pareja', anchor=CENTER)
tree.heading('#1', text='Jugador1', anchor=CENTER)
tree.heading('#2', text='Jugador 2', anchor=CENTER)
tree.heading('#3', text='Club', anchor=CENTER)

# Botones Borrar Editar
ttk.Button(text='Borra Pareja', command=borra_pareja).grid(
    row=7, column=0, sticky=W + E)
ttk.Button(text='Edita Pareja', command=edita_pareja).grid(
    row=7, column=1, sticky=W + E)

# Llenando la tabla
lee_pareja()


window.mainloop()
