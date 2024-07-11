from lib.clickUp.ClickUp import ClickUp
from lib.other.LocalmetricManager import Localmetric
from managers.models.__baseManager import __BaseManager
from datetime import datetime



class Fase1Manager(__BaseManager):
    def __init__(self, Localmetric: Localmetric, ClickUp: ClickUp) -> None:
        super().__init__(Localmetric, ClickUp)
        
        self.__Fase1Tasks: dict[str, dict[str, str]] = {
            'Fase 1': {
                'subtask-1': 'Análisis palabras clave.',
                'subtask-2': 'Análisis de las secciones de la ficha: zonas de servicio, categorias, descripción, menú, datos básicos.',
            },
            'Categorización sentimiento de cliente': {
                'subtask-1': 'Analizar reseñas.',
                'subtask-2': 'Detectar categorias de sentimientos y desarrollar 10 mensajes para cada categoria.',
                'subtask-3': 'Registrar categorización en el software: registrar todos los mensajes creados en la categorización.',
            },
            'Registrar carta/productos/servicios': {
                'description': 'Meter carta o dependiendo del cliente productos y/o servicios.',
            },
            'Crear plan de publicaciones': {
                'subtask-1': 'Crear 1 post por semana.',
            },
            'Analizar la posición del cliente': {
                'description': 'Una vez detectada la palabra clave principal, buscar en que posición está.',
            },
            'Extraer primer informe del sistema': {
                'description': 'Analizar en el sistema el informe previo a nuestra gestión. Dentro del sistema, en el boton de métricas',
            },
        }
    
    def __createFase1Tasks(self, listId: str):
        for task in self.__Fase1Tasks:
            newTaskId = self._ClickUp.Tasks.createOrUploadTaskInList(
                task, self.__Fase1Tasks[task].get('description', ''), {'Valentina', 'Javier Agote Lopez'}, listId,
                settings = {
                    'tags': ['fase 1'], 'priority': 3,
                    'due_date': int(datetime.now().timestamp()*1000) + 345600000, 'due_date_time': True,
                }, 
            )
            for subTask in self.__Fase1Tasks[task]:
                if subTask == 'description': continue
                self._ClickUp.Tasks.createOrUploadTaskInList(
                    self.__Fase1Tasks[task][subTask], '', {'Valentina Leandro', 'Javier Agote Lopez'}, listId,
                    settings = {
                        'due_date': int(datetime.now().timestamp()*1000) + 345600000, 'due_date_time': True,
                        'parent': newTaskId,
                    }, 
                )
        
    def createFase1ClientsLists(self) -> None:
        _allLists: dict[str, str] = {}
        for owner in self._ClientsOwners:
            _allLists.update(self._ClickUp.Lists.getListsInfo(self._ClientsFoldersID[owner]))
        for owner in self._ClientsOwners:
            for listName in set(self._ClientsOwners[owner]):
                if listName not in _allLists and listName not in self._ClientExceptions:
                    newListId = self._ClickUp.Lists.createLists(listName, self._ClientsFoldersID[owner], self._ClientExceptions)
                    self.__createFase1Tasks(newListId)