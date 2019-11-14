from tkinter import messagebox
import random
import sqlite3

# Funcion para ejecutar las preguntas a la BBDD


def run_query(query, parameters=()):
    with sqlite3.connect("BBDD_Domino") as conn:
        cursor = conn.cursor()
        result = cursor.execute(query, parameters)
        conn.commit()
    return result

# Trigger  para Insertar parejas en la tabla resultados


def parejas_total():
    # ---saber el numero de parejas totales incritas
    query = 'SELECT COUNT(pareja_inscrita) FROM Parejas'
    numero_parejas = run_query(query)
    for i in numero_parejas:
        total_parejas = i[0]
        resto = total_parejas % 2

        if resto == 0:
            numero_mesas = total_parejas//2
        else:
            numero_mesas = total_parejas//2+1

        # print(total_parejas)
        # print(numero_mesas)


query = ('''CREATE TRIGGER IF NOT EXISTS pareja_ai
                    AFTER INSERT 
                    ON Parejas
                    FOR EACH ROW
                        BEGIN
                            INSERT INTO Res_parejas (Npareja, Nombre_pareja)
                            VALUES (NEW.id, NEW.pareja_inscrita);
                        END''')
run_query(query, )

# Trigger  para Borrar parejas en la tabla resultados
query = ('''CREATE TRIGGER IF NOT EXISTS pareja_bd
                    BEFORE DELETE
                    ON Parejas
                    FOR EACH ROW
                        BEGIN
                            DELETE FROM Res_parejas WHERE Nombre_pareja==OLD.pareja_inscrita;
                        END''')
run_query(query, )
