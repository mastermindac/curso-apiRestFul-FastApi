import json
from models import Ingrediente
# Clase que nos permite trabajar con los datos de prueba
class FoodData:

    #Propiedades que almacenarán todos los datos
    alimentos=[]
    platos=[]
    fileAlimentos = None

    def __init__(self):
        #Carga de los ficheros de datos de prueba
        self.fileAlimentos=open('data/alimentos.json')
        self.alimentos = json.load(self.fileAlimentos)
        self.fileAlimentos.close()
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

        # Recibimos y guardamos un nuevo ingrediente
    async def write_ingrediente(self, ingrediente: Ingrediente):
        self.fileAlimentos=open('data/alimentos.json','w')
        #Conseguimos el último id de la lista
        ultimo_alimento=self.alimentos['alimentos'][-1]['id']
        #Añadimos un nuevo id al ingrediente nuevo
        ingredienteDict=ingrediente.model_dump()
        ingredienteDict['id']=ultimo_alimento+1
        self.alimentos['alimentos'].append(ingredienteDict)
        json.dump(self.alimentos,self.fileAlimentos,indent=2)
        self.fileAlimentos.close()
        return ingredienteDict

    

    # Recibimos y actualizamos un nuevo ingrediente
    async def update_ingrediente(self, ingrediente_id: int, ingrediente: Ingrediente):
        self.fileAlimentos=open('data/alimentos.json','w')
        #Buscamos el ingrediente
        ingredienteEncontrado=None
        ingredientePos=0
        #Recorremos todos los datos JSON
        for item in self.alimentos['alimentos']:
            #Comparamos el id que es int
            if item['id']==ingrediente_id:
                ingredienteEncontrado=item
                break
            ingredientePos=ingredientePos+1
        #Si se ha encontrado
        if(ingredienteEncontrado):
            #Realizamos la actualization
            ingredienteDict = ingrediente.model_dump()
            for elem in ingredienteDict:
                if(ingredienteDict[elem]):
                #cambiamos el valor
                    self.alimentos['alimentos'][ingredientePos][elem]=ingredienteDict[elem]
            json.dump(self.alimentos,self.fileAlimentos,indent=2)
            self.fileAlimentos.close()
            return self.alimentos['alimentos'][ingredientePos]
        else:
            return None

    # Borramos un ingrediente
    async def delete_ingrediente(self, ingrediente_id: int):
        self.fileAlimentos=open('data/alimentos.json','w')
        #Buscamos el ingrediente
        ingredienteEncontrado=None
        ingredientePos=0
        #Recorremos todos los datos JSON
        for item in self.alimentos['alimentos']:
            #Comparamos el id que es int
            if item['id']==ingrediente_id:
                ingredienteEncontrado=item
                break
            ingredientePos=ingredientePos+1
        #Si se ha encontrado
        if(ingredienteEncontrado):
            self.alimentos['alimentos'].pop(ingredientePos)
            json.dump(self.alimentos,self.fileAlimentos,indent=2)
            self.fileAlimentos.close()
            return {"info":"borrado ingrediente "+str(ingrediente_id)}
        else:
            return None


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