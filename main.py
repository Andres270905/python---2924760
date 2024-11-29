from fastapi import FastAPI, HTTPException, Depends
from conexion_db import crear_conexion
from models import Usuario, Producto, Factura, Mercancia, metodo_envio, met_pago, Detalle_Factura
from typing import List
from datetime import datetime, time, timedelta
import mysql.connector
from typing import Optional
import bcrypt
import jwt
from models import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)



def ejecutar_consulta(query: str, params: tuple = ()):
    conexion = mysql.connector.connect(host='localhost', database='seedweb', user='root', password='')
    if conexion is None:
        raise HTTPException(status_code=500, detail="Error al conectar a la base de datos")
    
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute(query, params)
        
       
        if query.strip().upper().startswith(("INSERT", "UPDATE", "DELETE")):
            conexion.commit()
            return cursor
        
        
        if query.strip().upper().startswith("SELECT"):
            results = cursor.fetchall()
            return results
        
    except mysql.connector.Error as e:
        conexion.rollback()
        raise HTTPException(status_code=500, detail=f"Error al ejecutar la consulta: {e}")
    finally:
        cursor.close()
        conexion.close()


#####      USUARIO      #####

@app.get("/usuarios", tags=['Usuarios'])
def obtener_usuarios():
    query = "SELECT * FROM usuario"
    usuarios = ejecutar_consulta(query)  
    return {"usuarios": usuarios} 

@app.post("/usuario", tags=['Usuarios'])
def crear_usuario(usuario: Usuario):
    
    query_check = "SELECT COUNT(*) FROM usuario WHERE id_usuario = %s"
    params_check = (usuario.id_usuario,)
    result = ejecutar_consulta(query_check, params_check)
    
    if result[0]["COUNT(*)"] > 0:
        raise HTTPException(status_code=400, detail=f"El id_usuario {usuario.id_usuario} ya existe.")
    
    
    query_insert = """INSERT INTO usuario (id_usuario, nombre_usuario, apellido_usuario, telefono_usuario, direccion, email, tipo_usuario, contrasena) 
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    params_insert = (
        usuario.id_usuario,  
        usuario.nombre_usuario, 
        usuario.apellido_usuario, 
        usuario.telefono_usuario,
        usuario.direccion, 
        usuario.email, 
        usuario.tipo_usuario.value,
        usuario.contrasena
    )

    
    resultado = ejecutar_consulta(query_insert, params_insert)  
    return {"mensaje": "Usuario creado exitosamente", "usuario": usuario.nombre_usuario}



@app.delete("/usuario/{id_usuario}", tags=["Usuarios"])
def eliminar_usuario(id_usuario: int):
    
    query = "DELETE FROM usuario WHERE id_usuario = %s"
    
   
    cursor = ejecutar_consulta(query, (id_usuario,))
    
   
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return {"mensaje": f"Usuario con id {id_usuario} eliminado exitosamente"}


@app.put("/usuario/{id_usuario}", tags=["Usuarios"])
def actualizar_usuario(id_usuario: int, usuario: Usuario):
    
    query_check = "SELECT COUNT(*) FROM usuario WHERE id_usuario = %s"
    params_check = (id_usuario,)
    result = ejecutar_consulta(query_check, params_check)

    
    if result[0]["COUNT(*)"] == 0:
        raise HTTPException(status_code=404, detail=f"Usuario con id {id_usuario} no encontrado")

   
    query_update = """UPDATE usuario 
                      SET nombre_usuario = %s, apellido_usuario = %s, telefono_usuario = %s, direccion = %s, 
                          email = %s, tipo_usuario = %s 
                      WHERE id_usuario = %s"""
    params_update = (
        usuario.nombre_usuario, 
        usuario.apellido_usuario, 
        usuario.telefono_usuario,
        usuario.direccion, 
        usuario.email, 
        usuario.tipo_usuario.value, 
        id_usuario 
    )

   
    ejecutar_consulta(query_update, params_update)

    return {"mensaje": f"Usuario con id {id_usuario} actualizado exitosamente", "usuario": usuario}

#####          PRODUCTOS          #####



@app.get("/productos", tags=['Productos'])
def obtener_productos():
    query = "SELECT * FROM productos"
    productos = ejecutar_consulta(query) 
    return {"productos": productos} 


@app.post("/producto", tags=['Productos'])
def crear_producto(producto: Producto):
    
    query_check = "SELECT COUNT(*) FROM productos WHERE id_producto = %s"
    params_check = (producto.id_producto,)
    result = ejecutar_consulta(query_check, params_check)
    
    
    if result[0]["COUNT(*)"] > 0:
        raise HTTPException(status_code=400, detail=f"El id_producto {producto.id_producto} ya existe.")
    
    
    query_insert = """INSERT INTO productos (id_producto, nombre_producto, descripcion, precio_producto, categoria, disponible) 
                      VALUES (%s, %s, %s, %s, %s, %s)"""
    params_insert = (
        producto.id_producto,  
        producto.nombre_producto, 
        producto.descripcion, 
        producto.precio_producto,
        producto.categoria.value, 
        producto.disponible
    )

    
    resultado = ejecutar_consulta(query_insert, params_insert)  
    return {"mensaje": "Producto creado exitosamente", "producto": producto}


@app.delete("/producto/{id_producto}", tags=["Productos"])
def eliminar_producto(id_producto: int):
    
    query = "DELETE FROM productos WHERE id_producto = %s"
    
    
    cursor = ejecutar_consulta(query, (id_producto,))
    
    
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    return {"mensaje": f"Producto con id {id_producto} eliminado exitosamente"}

@app.put("/producto/{id_producto}", tags=["Productos"])
def actualizar_producto(id_producto: int, producto: Producto):
    
    query_check = "SELECT COUNT(*) FROM productos WHERE id_producto = %s"
    params_check = (id_producto,)
    result = ejecutar_consulta(query_check, params_check)

   
    if result[0]["COUNT(*)"] == 0:
        raise HTTPException(status_code=404, detail=f"Producto con id {id_producto} no encontrado")

    
    query_update = """UPDATE productos 
                      SET nombre_producto = %s, descripcion = %s, precio_producto = %s, categoria = %s, 
                          disponible = %s 
                      WHERE id_producto = %s"""
    params_update = (
        producto.nombre_producto, 
        producto.descripcion, 
        producto.precio_producto,
        producto.categoria.value,  
        producto.disponible,
        id_producto  
    )

    
    ejecutar_consulta(query_update, params_update)

    return {"mensaje": f"Producto con id {id_producto} actualizado exitosamente", "producto": producto}


#####           MERCANCIA          #####


@app.get("/mercancia", tags=['Mercancia'])
def obtener_mercancia():
    query = "SELECT * FROM mercancia"
    mercancia = ejecutar_consulta(query)  
    return {"mercancia": mercancia}  



#####           METODO_ENVIO         #####


@app.get("/metodos_envio", tags=['Metodo Envio'])
def obtener_metodos_envio():
    query = "SELECT * FROM metodo_envio"
    metodos_envio = ejecutar_consulta(query)
    return {"metodos_envio": metodos_envio}


#####            FACTURA             #####




@app.get("/facturas", response_model=List[Factura], tags=["Facturas"])
async def obtener_facturas():
    query = "SELECT * FROM factura"
    facturas_db = ejecutar_consulta(query) 

   
    if not facturas_db:
        raise HTTPException(status_code=404, detail="No se encontraron facturas.")
    
    
    facturas = []
    for factura in facturas_db:
        
        if isinstance(factura['hora'], timedelta):
           
            total_seconds = factura['hora'].total_seconds()
            factura['hora'] = (datetime.min + timedelta(seconds=total_seconds)).time()

        
        facturas.append(Factura(**factura))  

    return facturas



#####        DETALLE_FACTURA           #####

@app.get("/detalle_factura", response_model=List[Detalle_Factura], tags=["Detalle Factura"])
def obtener_detalle_factura():
    query = """
        SELECT df.id_detalle_factura, df.id_mercancia, df.id_factura, 
               p.nombre_producto AS nombre_mercancia, f.fecha AS fecha_factura
        FROM detalle_de_factura df
        JOIN mercancia m ON df.id_mercancia = m.id_mercancia
        JOIN productos p ON m.id_producto = p.id_producto  -- Aquí se hace el JOIN con la tabla productos
        JOIN factura f ON df.id_factura = f.id_factura
    """
    
    
    detalles = ejecutar_consulta(query)
    
    
    if not detalles:
        raise HTTPException(status_code=404, detail="No se encontraron detalles de factura.")
    
    return detalles









