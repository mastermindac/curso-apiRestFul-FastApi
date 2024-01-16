from fastapi import FastAPI

# Objeto app de tipo FastApi
app = FastAPI()

#Configuracion del ApiRestFul

#Entrada GET http://localhost/
@app.get("/")
def read_root():
    return {"Hola": "Pakito"}


