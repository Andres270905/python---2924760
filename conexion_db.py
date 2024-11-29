import mysql.connector
from mysql.connector import Error

def crear_conexion():
    
    conexion = None  
    try:
        print("Intentando conectar a la base de datos...")
        
        conexion = mysql.connector.connect(
            host="localhost",       
            user="root",             
            password="",            
            database="seedweb"      
        )

        
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
            
            
            cursor = conexion.cursor()
            cursor.execute("SELECT DATABASE();")  
            db = cursor.fetchone()  
            print(f"Conectado a la base de datos: {db[0]}") 
            cursor.close()
            
            return conexion  
        else:
            print("Error al conectar a la base de datos")
            return None
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def cerrar_conexion(conexion):
   
    if conexion and conexion.is_connected():
        conexion.close()
        print("Conexión cerrada correctamente.")


conexion = crear_conexion()



