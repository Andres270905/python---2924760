from pydantic import BaseModel

# Modelo de datos para el Producto
class Producto(BaseModel):
    id: int
    nombre: str
    descripcion: str
    precio: float

# Modelo de entrada (sin id, ya que se asignará automáticamente)
class ProductoCreate(BaseModel):
    nombre: str
    descripcion: str
    precio: float