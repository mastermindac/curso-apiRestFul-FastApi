#importamos desde fastAPI, la clases FastAPI y Response
from typing import Union
from pydantic import BaseModel

# Modelo para la inserción de nuevos ingredientes
class Ingrediente(BaseModel):
    nombre: str
    calorias: Union[int, None] = None
    carbohidratos: Union[float, None] = None
    proteinas: Union[float, None] = None
    grasas: Union[float, None] = None
    fibra: Union[float, None] = None