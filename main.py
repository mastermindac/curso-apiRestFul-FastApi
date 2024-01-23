#importamos desde fastAPI, la clases FastAPI y Response
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
async def read_ingredients():
    #await pedir datos
    return await food.get_ingredientes()

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
