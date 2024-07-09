from lib.other.ClickUpAPI import ClickUp
from lib.other.LocalmetricManager import Localmetric
from datetime import datetime




class Manager:
    def __init__(self, Localmetric: Localmetric, ClickUp: ClickUp) -> None:
        self.__Localmetric = Localmetric
        self.__ClickUp = ClickUp

        self.__ClientsOwners: dict[str, list[str]] = Localmetric.getClientsOwners()
        self.__NegativeReviews: list[list[datetime | str | int]] = Localmetric.getNegativeReviewsFromOneMonth()
        self.__ClientsLocations: dict[str, str] = Localmetric.getClientsLocations()

        self.__ClientsFoldersID: dict[str, str] = ClickUp.getFoldersInfo(ClickUp.getSpacesInfo()['Clientes'])
        self.__FieldsID: dict[str, str] = ClickUp.getFieldsInfo(ClickUp.getListsInfo(self.__ClientsFoldersID['Localmetric'])['test *no borrar*'])    
        self.__ListsInfo: dict[str, str] = {}
        for owner in self.__ClientsOwners:
            self.__ListsInfo.update(ClickUp.getListsInfo(self.__ClientsFoldersID[owner]))
    
    def createClientsLists(self) -> None:
        for owner in self.__ClientsOwners:
            self.__ClickUp.createLists(set(self.__ClientsOwners[owner]), self.__ClientsFoldersID[owner])
    
    def createNegativeReviewsTasks(self) -> None:
        _clientsEmails: dict[str, str] = self.__Localmetric.getClientsEmails()
        
        for review in self.__NegativeReviews:
            listsTasksIdFields: dict[str, str] = self.__ClickUp.getTasksIdField(self.__ListsInfo[self.__ClientsLocations[review[1]]])

            email = _clientsEmails.get(review[8], _clientsEmails.get(review[7], ''))
            fieldValues: dict = {
                'Fecha reseña': [ ('value', review[0].timestamp()*1000), ('value_options', { 'time': True }) ], 'Dirección': [ ('value', review[6]) ],
                'Nombre ubicación': [ ('value', review[1]) ], 'id': [ ('value', review[5]) ], 'Email': [ ('value', email) ],
                'Nombre': [ ('value', review[2]) ], 'Puntuación': [ ('value', str(review[4])) ]
            }

            self.__ClickUp.createOrUploadTaskInList(
                f'Reseña negativa - {review[2]}', review[3], {'Miranda'},
                self.__ListsInfo[self.__ClientsLocations[review[1]]],
                settings = {
                    'tags': ['reseña'], 'priority': 3 if len(review[3]) < 200 else 2,
                    'due_date': int(datetime.now().timestamp()*1000) + 172800000, 'due_date_time': True,
                    "custom_fields": [
                        dict(fieldValues[field] + [ ('id', self.__FieldsID[field] ) ])
                        for field in self.__FieldsID
                    ]},
                method = ['put', listsTasksIdFields[review[5]]] if review[5] in listsTasksIdFields else ['get'], 
                )
    
    def removeRepliedReviewsTasks(self) -> None:
        _tasksIdFields: dict[str, str] = {}
        for list_ in self.__ListsInfo:
            _tasksIdFields.update(self.__ClickUp.getTasksIdField(self.__ListsInfo[list_]))
        
        _reviewsId: set[str] = set(review[5] for review in self.__NegativeReviews)
        for taskIdField in _tasksIdFields:
            if taskIdField not in _reviewsId:
                self.__ClickUp.deleteTaskOfList(_tasksIdFields[taskIdField])
        