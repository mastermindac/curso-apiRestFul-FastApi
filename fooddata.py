import json
# Clase que nos permite trabajar con los datos de prueba
class FoodData:

    #Propiedad que almacenará todos los alimentos
    alimentos=[]

    def __init__(self):
        #Carga del fichero de datos de prueba
        file=open('data/alimentos.json')
        self.alimentos = json.load(file)

    #Devolucion asincrona de datos de alimentos
    async def get_ingredientes(self):
        return self.alimentos

    # Devolucion asincrona de un alimento
    async def get_ingrediente(self,ingrediente_id: int):
        alimento={"error",str(ingrediente_id)+" no encontrado"}
        #Recorremos todos los datos JSON
        for item in self.alimentos['alimentos']:
            #Comparamos el id que es int
            if item['id']==ingrediente_id:
                alimento=item
                break
        return alimento