import json
import bcrypt
import os
from api.utilidades.models import Ingrediente, Plato, Usuario
# Clase que nos permite trabajar con los datos de prueba
class FoodData:

    #Propiedades que almacenarán todos los datos
    alimentos=[]
    platos=[]
    destacados = []
    usuarios = []
    fileAlimentos = None
    filePlatos = None
    fileDestacados = None
    fileUsuarios = None
    directorio_trabajo=None

    def __init__(self):
        self.directorio_trabajo = os.getcwd()
        self.directorio_trabajo=self.directorio_trabajo+"\\api\\data\\"
        #Carga de los ficheros de datos de prueba
        self.fileAlimentos=open(self.directorio_trabajo+'alimentos.json')
        self.alimentos = json.load(self.fileAlimentos)
        self.fileAlimentos.close()
        self.filePlatos=open(self.directorio_trabajo+'platos.json')
        self.platos = json.load(self.filePlatos)
        self.filePlatos.close()
        self.fileDestacados=open(self.directorio_trabajo+'destacados.json')
        self.destacados = json.load(self.fileDestacados)
        self.fileDestacados.close()
        self.fileUsuarios=open(self.directorio_trabajo+'usuarios.json')
        self.usuarios = json.load(self.fileUsuarios)
        self.fileUsuarios.close()

#INGREDIENTES
    #Devolucion asincrona de datos de alimentos
    async def get_ingredientes(self,skip,total,filtronombre):
        alimentos=[]
        #si existe filtronombre nos quedamos con aquellos que contengan ese filtro
        if(filtronombre):
            for item in self.alimentos['alimentos'][skip:(total+skip)]:
                # Comparamos el id que es int
                if filtronombre in item['nombre']:
                    alimentos.append(item)
        else:
            alimentos = self.alimentos['alimentos'][skip:(total+skip)]
        return {'alimentos':alimentos}
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
        self.fileAlimentos=open(self.directorio_trabajo+'alimentos.json', 'w')
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
        self.fileAlimentos=open(self.directorio_trabajo+'alimentos.json', 'w')
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
        self.fileAlimentos=open(self.directorio_trabajo+'alimentos.json', 'w')
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

    # Recibimos y guardamos un nuevo plato junto a un nuevo ingrediente
    async def write_ingredientePlato(self, ingrediente: Ingrediente,plato: Plato):
        ingrediente = await self.write_ingrediente(ingrediente)
        #Serializamos para añadir id
        platoDict = plato.model_dump()
        platoDict['ingredientes'][0]['id']=ingrediente['id']
        platoIngredienteConId=Plato.model_validate(platoDict)
        platoDict = await self.write_plato(platoIngredienteConId)
        return dict([('ingrediente',ingrediente),('plato',platoDict)])

#PLATOS
    #Devolucion asincrona de datos de platos
    async def get_platos(self,skip,total,filtronombre):
        platos=[]
        #si existe filtronombre nos quedamos con aquellos que contengan ese filtro
        if(filtronombre):
            for item in self.platos['platos'][skip:(total+skip)]:
                # Comparamos el id que es int
                if filtronombre in item['nombre']:
                    platos.append(item)
        else:
            platos = self.platos['platos'][skip:(total+skip)]
        return {'alimentos':platos}
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

    # Recibimos y guardamos un nuevo plato
    async def write_plato(self, plato: Plato,tiempoDestacado: int):
        self.filePlatos=open(self.directorio_trabajo+'platos.json', 'w')
        #Conseguimos el último id de la lista
        ultimo_plato=self.platos['platos'][-1]['id']
        #Añadimos un nuevo id al ingrediente nuevo
        platoDict=plato.model_dump()
        platoDict['id']=ultimo_plato+1
        self.platos['platos'].append(platoDict)
        json.dump(self.platos,self.filePlatos,indent=2)
        self.filePlatos.close()
        #Añadimos a destacado
        destacadoDict=await self.write_destacado(platoDict,tiempoDestacado)
        return dict([('plato',platoDict),('destacado',destacadoDict)])

    #DESTACADOS
    # Añadimos un nuevo plato destacado
    async def write_destacado(self, plato: Plato, tiempoDestacado:int):
        self.fileDestacados=open(self.directorio_trabajo+'destacados.json', 'w')
        #Conseguimos el último id de la lista
        ultimo_destacado=self.destacados['destacados'][-1]['id']
        #Añadimos un nuevo destacado
        destacadoDict = {}
        destacadoDict['id']=ultimo_destacado+1
        destacadoDict['id_plato'] = plato['id']
        destacadoDict['tiempo'] = tiempoDestacado
        self.destacados['destacados'].append(destacadoDict)
        json.dump(self.destacados,self.fileDestacados,indent=2)
        self.fileDestacados.close()
        return destacadoDict

    # USUARIOS
    # Recibimos y guardamos un nuevo usuario
    async def write_usuario(self, usuario: Usuario):
        self.fileUsuarios=open(self.directorio_trabajo+'usuarios.json', 'w')
        #Conseguimos el último id de la lista
        ultimo_usuario=self.usuarios['usuarios'][-1]['id']
        #Añadimos un nuevo id
        usuarioDict=usuario.model_dump()
        usuarioDict['id']=ultimo_usuario+1
        # Hash del password
        salt = bcrypt.gensalt()
        usuarioDict['password'] = bcrypt.hashpw(usuarioDict['password'].encode('utf-8'), salt).decode("utf-8")
        self.usuarios['usuarios'].append(usuarioDict)
        json.dump(self.usuarios,self.fileUsuarios,indent=2)
        self.fileUsuarios.close()
        return usuarioDict