from fastapi import APIRouter
from typing import Union, Annotated
from fastapi import Response, status, Query, Path, HTTPException
from api import Ingrediente, Plato
from api import FoodData


# Objeto para trabajar con los datos de prueba
food = FoodData()
router = APIRouter()

#INGREDIENTES
@router.get("")
async def read_ingredients(total: Annotated[int,
                                            Query(description="Total de ingredientes a devolver")],
                           skip:int=0,todos: Union[bool, None] = None,
                           filtronombre: Annotated[Union[str, None],
                                         Query(
                                             description="Filtro de busqueda",
                                             min_length=3,
                                             max_length=10)] = None):

    #await pedir datos
    if(todos):
        return await food.get_allIngredientes()
    else:
        return await food.get_ingredientes(skip, total,filtronombre)
@router.get("/{ingrediente_id}", status_code=status.HTTP_200_OK,
         summary="Buscar Ingrediente",
         description="Buscar Ingrediente a través del ingrtediente_id"
         )
async def read_ingredient(ingrediente_id: Annotated[int, Path(description="Id entero de busqueda",ge=0)],
                          response: Response):
    # Buscamos el ingrediente
    ingrediente=await food.get_ingrediente(ingrediente_id)
    #Si no encontramos el plato devolvemos error
    if not ingrediente:
        raise HTTPException(status_code=404, detail="Ingrediente "+str(ingrediente_id)+" no encontrado")
    return ingrediente

@router.post("")
async def write_ingredients(ingrediente:Ingrediente):
    return await food.write_ingrediente(ingrediente)

@router.put("/{ingrediente_id}")
async def update_ingredients(ingrediente_id:int,ingrediente:Ingrediente):
    return await food.update_ingrediente(ingrediente_id,ingrediente)

@router.delete("/{ingrediente_id}")
async def delete_ingredients(ingrediente_id:int):
    return await food.delete_ingrediente(ingrediente_id)

@router.post("/ingredientesplatos")
async def write_ingredientsplatos(ingrediente:Ingrediente,plato:Plato):
    return await food.write_ingredientePlato(ingrediente,plato)
