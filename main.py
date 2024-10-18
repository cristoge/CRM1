import mysql.connector  # Importem el connector per treballar amb MySQL.

def connectar_bbdd():
    try:
        connection = mysql.connector.connect(
            host="localhost",  # L'adreça del servidor MySQL, en aquest cas, s'utilitza 'localhost'.
            database="crm",  # El nom de la base de dades amb la qual volem treballar.
            user="root",  # Nom d'usuari de MySQL. En aquest cas, és 'root', l'usuari per defecte.
            password="root"  # La contrasenya de MySQL per a l'usuari 'root'.
        )
        return connection  # Si la connexió té èxit, es retorna l'objecte de connexió.
    except mysql.connector.Error as error:
        print(f"Error en la connexió: {error}")  # En cas d'error, s'imprimeix el missatge de l'error.
        return None  # Si falla, es retorna 'None', indicant que no s'ha pogut connectar.
