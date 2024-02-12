#importamos desde fastAPI, la clases FastAPI y Response
from typing import Union
from pydantic import BaseModel, Field
from enum import Enum


class TipoPlato(str, Enum):
    entrante = "entrante"
    principal = "principal"
    postre = "postre"
    bebida = "bebida"


# Modelo para la inserción de nuevos ingredientes
class Ingrediente(BaseModel):
    nombre: str
    calorias: Union[int, None] = Field(default=None, gt=0, description="Calorías del ingrediente. Entero mayor que 0")
    carbohidratos: Union[float, None] = None
    proteinas: Union[float, None] = None
    grasas: Union[float, None] = None
    fibra: Union[float, None] = None

# Modelo para la inserción de nuevo plato
class IngredientePlato(BaseModel):
    id: int
    cant: int
    ud: str
class Plato(BaseModel):
    nombre:  str = Field(description="Nombre del plato", max_length=128)
    tipo: TipoPlato
    ingredientes: list[IngredientePlato]

# Modelo de Usuarios
class Usuario(BaseModel):
    nombre: str
    apellidos: str
    email: str
    password: str

class UsuarioOut(BaseModel):
    nombre: str
    apellidos: str
    email: str
