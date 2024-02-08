#importamos desde fastAPI, la clases FastAPI y Response
import json
from typing import Union, Annotated
from fastapi import FastAPI, Response, status, Body, Query, Path, HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from docs import tags_metadata
from fooddata import FoodData
from models import Ingrediente, Plato
from fastapi.responses import JSONResponse

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

#Las excecpciones de Errores modificadas
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error":exc.detail},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    #Conversion dict
    errorDict=eval(str(exc))
    #MAnejamos diferentes códigos
    if(errorDict[0]['type']=='greater_than_equal'):
        codigoError=422
    else:
        codigoError = 404
    return JSONResponse(
        status_code=codigoError,
        content={
            "error":errorDict[0]['msg'],
            "datoEnviado":errorDict[0]['input']
        },
    )
#Definición de los ENDPOINTS

#DEFAULT
@app.get("/")
def read_root():
    return {"Hola": "Pakito"}

#INGREDIENTES
@app.get("/ingredientes",tags=["ingredientes"])
async def read_ingredients(total:int,skip:int=0,todos: Union[bool, None] = None,
                           filtronombre: Annotated[Union[str, None],
                                         Query(min_length=3, max_length=10)] = None):

    #await pedir datos
    if(todos):
        return await food.get_allIngredientes()
    else:
        return await food.get_ingredientes(skip, total,filtronombre)
@app.get("/ingredientes/{ingrediente_id}",tags=["ingredientes"], status_code=status.HTTP_200_OK)
async def read_ingredient(ingrediente_id: Annotated[int, Path(ge=0)],
                          response: Response):
    # Buscamos el ingrediente
    ingrediente=await food.get_ingrediente(ingrediente_id)
    #Si no encontramos el plato devolvemos error
    if not ingrediente:
        raise HTTPException(status_code=404, detail="Ingrediente "+str(ingrediente_id)+" no encontrado")
    return ingrediente

@app.post("/ingredientes",tags=["ingredientes"])
async def write_ingredients(ingrediente:Ingrediente):
    return await food.write_ingrediente(ingrediente)

@app.put("/ingredientes/{ingrediente_id}",tags=["ingredientes"])
async def update_ingredients(ingrediente_id:int,ingrediente:Ingrediente):
    return await food.update_ingrediente(ingrediente_id,ingrediente)

@app.delete("/ingredientes/{ingrediente_id}",tags=["ingredientes"])
async def delete_ingredients(ingrediente_id:int):
    return await food.delete_ingrediente(ingrediente_id)

@app.post("/ingredientesplatos",tags=["ingredientes"])
async def write_ingredientsplatos(ingrediente:Ingrediente,plato:Plato):
    return await food.write_ingredientePlato(ingrediente,plato)

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
    #Si no encontramos el plato devolvemos error
    if not plato:
        raise HTTPException(status_code=404, detail="Plato "+str(plato_id)+" no encontrado")
    return ingrediente

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

@app.post("/platos",tags=["platos"])
async def write_platos(plato:Plato, tiempodestacado: Annotated[int, Body()]):
    return await food.write_plato(plato,tiempodestacado)


