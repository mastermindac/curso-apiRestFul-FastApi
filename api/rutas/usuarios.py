from fastapi import APIRouter
from typing import Any
from fastapi import BackgroundTasks
from api import Usuario, UsuarioOut
from api import FoodData


# Objeto para trabajar con los datos de prueba
food = FoodData()
router = APIRouter()

#USUARIOS
def enviar_correo_fake(email: str, message=""):
    with open("../log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)
@router.post("",response_model=UsuarioOut)
async def write_usuario(usuario:Usuario,backgroundTasks: BackgroundTasks) -> Any:
    #Tarea en BG
    backgroundTasks.add_task(enviar_correo_fake, "paco@paco.es", message="Nuestro primer correo fake")
    return await food.write_usuario(usuario)