from lib.clickUp.ClickUp import ClickUp
from lib.other.LocalmetricManager import Localmetric
from datetime import datetime, timedelta
from managers.models.__baseManager import __BaseManager



class ReviewsManager(__BaseManager):
    def __init__(self, Localmetric: Localmetric, ClickUp: ClickUp) -> None:
        super().__init__()
        
        self.__NegativeReviews: list[list[datetime | str | int]] = Localmetric.getNegativeReviewsFromOneMonth()
        self.__ClientsLocations: dict[str, str] = Localmetric.getClientsLocations()

        self.__FieldsID: dict[str, str] = ClickUp.Fields.getFieldsInfo(ClickUp.getListsInfo(self.__ClientsFoldersID['Localmetric'])['test *no borrar*'])    
        self.__ListsInfo: dict[str, str] = {}
        self.__TasksFields: dict[str, dict[str, str]] = {}
        for owner in self.__ClientsOwners:
            self.__ListsInfo.update(ClickUp.Lists.getListsInfo(self.__ClientsFoldersID[owner]))
        for list_ in self.__ListsInfo:
            self.__TasksFields.update(self.__ClickUp.Tasks.getTasksFields(self.__ListsInfo[list_]))
    
    def createNegativeReviewsTasks(self) -> None:
        _clientsEmails: dict[str, str] = self.__Localmetric.getClientsEmails()
        
        for review in self.__NegativeReviews:
            if self.__ClientsLocations[review[1]] in self.__ClientExceptions or review[5] in self.__TasksFields:
                continue

            email = _clientsEmails.get(review[7], _clientsEmails.get(review[8], ''))
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
                        dict(fieldValues[field] + [ ('id', self.__FieldsID[field]) ])
                        for field in self.__FieldsID
                    ]}, 
                )
    
    def removeRepliedReviewsTasks(self) -> None:    
        _reviewsId: set[str] = set(review[5] for review in self.__NegativeReviews)
        for task in self.__TasksFields:
            if task not in _reviewsId:
                self.__ClickUp.Tasks.deleteTaskOfList(self.__TasksFields[task]['id'])
            elif datetime.fromtimestamp(int(self.__TasksFields[task]['Fecha reseña']) / 1000) <= (datetime.now() - timedelta(days=7)):
                self.__ClickUp.Tasks.updateTask(self.__TasksFields[task]['id'], { 'priority': 1 })