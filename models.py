#importamos desde fastAPI, la clases FastAPI y Response
from typing import Union
from pydantic import BaseModel
from enum import Enum


class TipoPlato(str, Enum):
    entrante = "entrante"
    principal = "principal"
    postre = "postre"
    bebida = "bebida"


# Modelo para la inserción de nuevos ingredientes
class Ingrediente(BaseModel):
    nombre: str
    calorias: Union[int, None] = None
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
    nombre: str
    tipo: TipoPlato
    ingredientes: list[IngredientePlato]

