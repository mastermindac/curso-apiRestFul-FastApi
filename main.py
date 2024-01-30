#importamos desde fastAPI, la clases FastAPI y Response
from typing import Union
from fastapi import FastAPI, Response, status
from docs import tags_metadata
from fooddata import FoodData

# Objeto para trabajar con los datos de prueba
food = FoodData()

# Objeto app de tipo FastApi
app = FastAPI(
    title="FoodAPI",
    description="ApiRestFul para la gestión de alimentos y planes nutricionales",
    version="0.0.2",
    contact={
        "name":"Paco Gómez",
        "url":"http://www.mastermind.ac"
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata
)

#Definición de los ENDPOINTS

#DEFAULT
@app.get("/")
def read_root():
    return {"Hola": "Pakito"}

#INGREDIENTES
@app.get("/ingredientes",tags=["ingredientes"])
async def read_ingredients(total:int,skip:int=0,todos: Union[bool, None] = None):
    #await pedir datos
    if(todos):
        return await food.get_allIngredientes()
    else:
        return await food.get_ingredientes(skip, total)
@app.get("/ingredientes/{ingrediente_id}",tags=["ingredientes"], status_code=status.HTTP_200_OK)
async def read_ingredient(ingrediente_id: int,response: Response):
    # Buscamos el ingrediente
    ingrediente=await food.get_ingrediente(ingrediente_id)
    #Si encontramos el ingrediente lo devolvemos
    if(ingrediente):
        return ingrediente
    #Si el ingrediente es nulo
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error",str(ingrediente_id)+" no encontrado"}

@app.post("/ingredientes",tags=["ingredientes"])
async def write_ingredients():
    return {"ingrediente":"POST"}

#PLATOS
@app.get("/platos",tags=["platos"])
async def read_platos(total:int,skip:int=0,todos: Union[bool, None] = None):
    #await pedir datos
    if(todos):
        return await food.get_allPlatos()
    else:
        return await food.get_platos(skip, total)
@app.get("/platos/{plato_id}",tags=["platos"], status_code=status.HTTP_200_OK)
async def read_plato(plato_id: int,response: Response):
    # Buscamos el plato
    plato=await food.get_plato(plato_id)
    #Si encontramos el ingrediente lo devolvemos
    if(plato):
        return plato
    #Si el ingrediente es nulo
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error",str(plato_id)+" no encontrado"}

@app.get("/platos/{plato_id}/ingredientes/{ingrediente_id}",tags=["platos"], status_code=status.HTTP_200_OK)
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

