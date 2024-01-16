from fastapi import FastAPI

# Objeto app de tipo FastApi
app = FastAPI()

#Configuracion del ApiRestFul

#Endpoint GET /
@app.get("/")
def read_root():
    return {"Hola": "Pakito"}

#Endpoint GET /ingredientes
@app.get("/ingredientes")
def read_ingredients():
    return {"Objeto": "Ingredientes"}


