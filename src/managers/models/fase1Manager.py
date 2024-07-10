from lib.clickUp.ClickUp import ClickUp
from lib.other.LocalmetricManager import Localmetric
from managers.models.__baseManager import __BaseManager



class Fase1Manager(__BaseManager):
    def __init__(self, Localmetric: Localmetric, ClickUp: ClickUp) -> None:
        super().__init__(Localmetric, ClickUp)
        
    def createClientsLists(self) -> None:
        for owner in self.__ClientsOwners:
            self.__ClickUp.Lists.createLists(set(self.__ClientsOwners[owner]), self.__ClientsFoldersID[owner], self.__ClientExceptions)