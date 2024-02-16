import uvicorn
#importamos desde fastAPI, la clases FastAPI y Response
from typing import Any,Union, Annotated
from fastapi import FastAPI, Response, status, Body, Query, Path, HTTPException, BackgroundTasks
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from api import FoodData, platosrutas, ingredientesrutas, usuariosrutas
from api.docs import tags_metadata
from api import Ingrediente, Plato, Usuario, UsuarioOut
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
app.include_router(
    ingredientesrutas,
    tags=["ingredientes"],
    prefix="/ingredientes",
)
#PLATOS
app.include_router(
    platosrutas,
    tags=["platos"],
    prefix="/platos",
)
#USUARIOS
app.include_router(
    usuariosrutas,
    tags=["usuarios"],
    prefix="/usuarios",
)



#DEBUGING
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)