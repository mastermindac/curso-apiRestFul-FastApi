from fastapi import APIRouter
from typing import Union, Annotated
from fastapi import Response, status, Body, HTTPException
from api import Plato
from api import FoodData


# Objeto para trabajar con los datos de prueba
food = FoodData()
router = APIRouter()

#PLATOS
@router.get("")
async def read_platos(total:int,skip:int=0,todos: Union[bool, None] = None):
    #await pedir datos
    if(todos):
        return await food.get_allPlatos()
    else:
        return await food.get_platos(skip, total)
@router.get("/{plato_id}", status_code=status.HTTP_200_OK)
async def read_plato(plato_id: int,response: Response):
    # Buscamos el plato
    plato=await food.get_plato(plato_id)
    #Si no encontramos el plato devolvemos error
    if not plato:
        raise HTTPException(status_code=404, detail="Plato "+str(plato_id)+" no encontrado")
    return plato

@router.get("/{plato_id}/ingredientes/{ingrediente_id}", status_code=status.HTTP_200_OK)
async def read_platoIngrediente(plato_id: int,ingrediente_id: int,response: Response):
    # Buscamos el plato
    ingrediente=await food.get_ingredientePlato(plato_id,ingrediente_id)
    #Si encontramos el ingrediente lo devolvemos
    if(ingrediente):
        return ingrediente
    #Si el ingrediente es nulo
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error","plato "+str(plato_id)+","+"ingrediente "+str(ingrediente_id)+" no encontrado"}

@router.post("")
async def write_platos(plato:Plato, tiempodestacado: Annotated[int, Body()]):
    return await food.write_plato(plato,tiempodestacado)
