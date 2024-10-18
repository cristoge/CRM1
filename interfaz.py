import tkinter as tk
from tkinter import ttk
from main import connectar_bbdd
import csv


def inserir_venda():
    connection = connectar_bbdd()  # Es connecta a la base de dades.
    if connection:  # Si la connexió ha estat exitosa:
        cursor = connection.cursor()  # Crea un cursor per executar consultes SQL.
        query = "INSERT INTO vendes (producte, quantitat, preu, data_venda) VALUES (%s, %s, %s, %s)"  # Consulta SQL.
        dades = (
            entrada_producte.get(),
            entrada_quantitat.get(),
            entrada_preu.get(),
            entrada_data.get(),
        )  # Recullem les dades dels camps d'entrada.
        cursor.execute(
            query, dades
        )  # Executem la consulta amb les dades proporcionades.
        connection.commit()  # Guardem els canvis a la base de dades.
        cursor.close()  # Tanquem el cursor.
        connection.close()  # Tanquem la connexió.
        actualitzar_treeview()  # Actualitzem la taula per mostrar les noves dades.


def actualitzar_treeview():
    for fila in tree.get_children():
        tree.delete(
            fila
        )  # Elimina totes les files actuals del Treeview per actualitzar les dades.

    connection = connectar_bbdd()  # Es connecta a la base de dades MySQL.
    if connection:  # Si la connexió té èxit:
        cursor = connection.cursor()  # Crea un cursor per executar consultes SQL.
        cursor.execute(
            "SELECT producte, quantitat, preu, data_venda FROM vendes"
        )  # Executa una consulta per obtenir totes les vendes.
        files = (
            cursor.fetchall()
        )  # Reculleix totes les files retornades per la consulta.

        # Itera per cada fila obtinguda de la consulta i les insereix al Treeview.
        for fila in files:
            tree.insert("", tk.END, values=fila)  # Insereix les dades al Treeview.

        cursor.close()  # Tanca el cursor.
        connection.close()  # Tanca la connexió amb la base de dades.


def mostrar_datos(datos):
    """
    Modificación que obtiene los valores del item seleccionado
    al hacer clic en el Treeview y los inserta en los campos de entrada.
    """
    # Obtiene el item seleccionado.
    selection = tree.selection()

    # Se verifica que si hay un error en la seleccion no pete el programa
    if not selection:
        return
    # Se obtiene el primer item seleccionado
    selected_item = selection[0]
    # Obtiene los valores del item seleccionado.
    valores = tree.item(selected_item, "values")

    # Lista de campos de entrada.
    campos = [entrada_producte, entrada_quantitat, entrada_preu, entrada_data]

    # Limpia e inserta los valores en los campos de entrada
    # Con el zip puedo hacer un for de los campos y los valores
    for campo, valor in zip(campos, valores):
        campo.delete(0, tk.END)  # Limpia el campo. Convencion de tkinter
        campo.insert(0, valor)  # Inserta el nuevo valor. Convencion de tkinter


def actualitzar_venda():
    """
    Ampliacion 1

    Igual que en el ejemplo de inserir
    lo que cambia es la query que en
    este caso es UPDATE
    """
    connection = connectar_bbdd()
    if connection:
        cursor = connection.cursor()
        query = "UPDATE vendes SET producte = %s, quantitat = %s, preu = %s, data_venda = %s WHERE producte = %s"
        dades = (
            entrada_producte.get(),
            entrada_quantitat.get(),
            entrada_preu.get(),
            entrada_data.get(),
            entrada_producte.get(),
        )
        cursor.execute(query, dades)
        connection.commit()
        cursor.close()
        connection.close()
        actualitzar_treeview()


def eliminar_venda():
    """
    Ampliacion 2 de las actualizaciones de la venta
    Igual que en el proceso de inserir lo unico que
    cambia es la query que en este caso es DELETE
    """
    connection = connectar_bbdd()  # Es connecta a la base de dades.
    if connection:
        cursor = connection.cursor()
        query = "DELETE FROM vendes WHERE producte = %s"
        dades = (entrada_producte.get(),)
        cursor.execute(query, dades)
        connection.commit()  # Guardem els canvis a la base de dades.
        cursor.close()  # Tanquem el cursor.
        connection.close()  # Tanquem la connexió.
        actualitzar_treeview()  # Actualitzem la taula per mostrar les noves dades.


def generar_informe_csv():
    """
    Ampliacion 3 que estaba en el word.
    """
    connection = connectar_bbdd()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT producte, quantitat, preu, data_venda FROM vendes")
        files = cursor.fetchall()

        # Escriu les dades en un fitxer CSV
        with open("informe_vendes.csv", mode="w", newline="") as fitxer_csv:
            escriptor_csv = csv.writer(fitxer_csv)
            escriptor_csv.writerow(
                ["Producte", "Quantitat", "Preu", "Data de Venda"]
            )  # Capçalera
            escriptor_csv.writerows(files)  # Escriu totes les files

        cursor.close()
        connection.close()
        print("Informe CSV generat correctament.")


root = tk.Tk()  # Crea la finestra principal de l'aplicació.
root.title("Gestió de Vendes")  # Defineix el títol de la finestra.

# Etiquetes i caixes de text per inserir informació de la venda.
tk.Label(root, text="Producte").grid(
    row=0, column=0
)  # Etiqueta "Producte" a la fila 0 i columna 0.
entrada_producte = tk.Entry(root)  # Crea un camp d'entrada de text per al producte.
entrada_producte.grid(
    row=0, column=1
)  # Ubica el camp d'entrada a la fila 0 i columna 1.

tk.Label(root, text="Quantitat").grid(
    row=1, column=0
)  # Etiqueta "Quantitat" a la fila 1 i columna 0.
entrada_quantitat = tk.Entry(root)  # Crea un camp d'entrada per la quantitat.
entrada_quantitat.grid(
    row=1, column=1
)  # Ubica el camp d'entrada a la fila 1 i columna 1.

tk.Label(root, text="Preu").grid(
    row=2, column=0
)  # Etiqueta "Preu" a la fila 2 i columna 0.
entrada_preu = tk.Entry(root)  # Crea un camp d'entrada per al preu.
entrada_preu.grid(row=2, column=1)  # Ubica el camp d'entrada a la fila 2 i columna 1.

tk.Label(root, text="Data de Venda").grid(
    row=3, column=0
)  # Etiqueta "Data de Venda" a la fila 3 i columna 0.
entrada_data = tk.Entry(root)  # Crea un camp d'entrada per la data de la venda.
entrada_data.grid(row=3, column=1)  # Ubica el camp d'entrada a la fila 3 i columna 1.


# Taula (Treeview) per mostrar les vendes.
tree = ttk.Treeview(
    root, columns=("producte", "quantitat", "preu", "data"), show="headings"
)
tree.heading("producte", text="Producte")  # Defineix el títol de la columna "Producte".
tree.heading(
    "quantitat", text="Quantitat"
)  # Defineix el títol de la columna "Quantitat".
tree.heading("preu", text="Preu")  # Defineix el títol de la columna "Preu".
tree.heading(
    "data", text="Data de Venda"
)  # Defineix el títol de la columna "Data de Venda".
tree.grid(
    row=4, column=0, columnspan=2
)  # Ubica la taula a la fila 4 i fa que ocupi dues columnes.


# Vincula el evento de la seleccion con el boton izquierdo del raton.
tree.bind("<ButtonRelease-1>", mostrar_datos)


"""
Botones apilados uno encima de otro
El primero es el que ya nos daba en el word
El segundo es el boton que añadi para poder ver los datos
El tercero es el boton para actualizar los datos, la primera ampliacion
El cuarto es el boton para eliminar los datos, la segunda ampliacion
El quinto es el boton para generar un informe csv, la tercera ampliacion
"""
boto_inserir = tk.Button(root, text="Insertar Venda", command=inserir_venda)
boto_inserir.grid(row=5, column=0, columnspan=2)
boto_mostrar = tk.Button(root, text="Mostrar Vendes", command=actualitzar_treeview)
boto_mostrar.grid(row=6, column=0, columnspan=2)
boto_actualitzar = tk.Button(root, text="Actualitzar Venda", command=actualitzar_venda)
boto_actualitzar.grid(row=7, column=0, columnspan=2)
boto_eliminar = tk.Button(root, text="Eliminar Venda", command=eliminar_venda)
boto_eliminar.grid(row=8, column=0, columnspan=2)
boto_generar_informe = tk.Button(
    root, text="Generar Informe CSV", command=generar_informe_csv
)
boto_generar_informe.grid(row=9, column=0, columnspan=2)
root.mainloop()  # Inicia la interfície gràfica i espera interaccions de l'usuari.
