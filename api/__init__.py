from api.data.fooddata import FoodData
from api.utilidades.models import Ingrediente, Plato, Usuario, UsuarioOut
from api.rutas.platos import router as platosrutas
from api.rutas.ingredientes import router as ingredientesrutas
from api.rutas.usuarios import router as usuariosrutas

from api.main import app