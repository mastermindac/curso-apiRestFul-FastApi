import json
# Clase que nos permite trabajar con los datos de prueba
class FoodData:

    #Propiedades que almacenarán todos los datos
    alimentos=[]
    platos=[]

    def __init__(self):
        #Carga de los ficheros de datos de prueba
        fileAlimentos=open('data/alimentos.json')
        self.alimentos = json.load(fileAlimentos)
        filePlatos=open('data/platos.json')
        self.platos = json.load(filePlatos)

#INGREDIENTES
    #Devolucion asincrona de datos de alimentos
    async def get_ingredientes(self,skip,total):
        return {'alimentos':self.alimentos['alimentos'][skip:(total+skip)]}
    async def get_allIngredientes(self):
        return self.alimentos

    # Devolucion asincrona de un alimento
    async def get_ingrediente(self,ingrediente_id: int):
        # Código antiguo
        # alimento={"error",str(ingrediente_id)+" no encontrado"}
        # alimento se inicializa a nulo
        # si no se encuentra el alimento se devolverá el nulo en vez de un objeto JSON
        alimento=None
        #Recorremos todos los datos JSON
        for item in self.alimentos['alimentos']:
            #Comparamos el id que es int
            if item['id']==ingrediente_id:
                alimento=item
                break
        return alimento

#PLATOS
    #Devolucion asincrona de datos de alimentos
    async def get_platos(self,skip,total):
        return {'platos':self.platos['platos'][skip:(total+skip)]}
    async def get_allPlatos(self):
        return self.platos

    # Devolucion asincrona de un alimento
    async def get_plato(self,plato_id: int):
        plato=None
        #Recorremos todos los datos JSON
        for item in self.platos['platos']:
            #Comparamos el id que es int
            if item['id']==plato_id:
                plato=item
                break
        return plato

    async def get_ingredientePlato(self,plato_id: int,ingrediente_id: int):
        plato=await self.get_plato(plato_id)
        ingrediente=None
        if(plato):
            for item in plato['ingredientes']:
                # Comparamos el id que es int
                if item['id'] == ingrediente_id:
                    ingrediente = await self.get_ingrediente(ingrediente_id)
                    break
        return ingrediente