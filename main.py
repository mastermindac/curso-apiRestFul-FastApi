from fastapi import FastAPI
from docs import tags_metadata

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

#Configuracion del ApiRestFul

#Endpoint GET /
@app.get("/")
def read_root():
    return {"Hola": "Pakito"}

#Endpoint GET /ingredientes
@app.get("/ingredientes",tags=["ingredientes"])
def read_ingredients():
    return {"Objeto": "Ingredientes"}
