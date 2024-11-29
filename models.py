from typing import Optional, Set
from pydantic import BaseModel, HttpUrl, Field, EmailStr
from enum import Enum
from typing import Optional
from datetime import date, time 




class tp_usuario(Enum):
    vendedor = 'vendedor'
    comprador = 'comprador'
   
    
class Usuario(BaseModel):
    id_usuario: int
    nombre_usuario: str
    apellido_usuario: str
    telefono_usuario: str
    direccion: str
    email: EmailStr
    tipo_usuario: tp_usuario 
    contrasena: str
     

class categoria_producto(Enum):
    frutas = "frutas"
    verduras = "verduras"
    tuberculos = "tuberculos"
    

class Producto(BaseModel):
    id_producto: int
    nombre_producto: str
    descripcion: str
    precio_producto: int
    categoria: categoria_producto
    disponible: int


class Mercancia(BaseModel):
    id_mercancia: int
    id_producto: int
    id_usuario: int

class met_envio(Enum):
    Domicilio = "Domicilio"
    Punto_de_entrega = "Punto_de_entrega"

class metodo_envio(BaseModel):
    id_pedido: int
    metodo: met_envio



class met_pago(Enum):
    efectivo = "efectivo"
    tarjeta = "tarjeta"
    pse = "pse"


class Factura(BaseModel):
    id_factura: int
    fecha: date       
    hora: time       
    cantidad: int
    medio_de_pago: met_pago



class Detalle_Factura(BaseModel):
    id_detalle_factura: int
    id_mercancia: int
    id_factura: int



























    
    