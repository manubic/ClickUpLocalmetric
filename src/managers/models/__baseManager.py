from lib.clickUp.ClickUp import ClickUp
from lib.other.LocalmetricManager import Localmetric



class __BaseManager:
    def __init__(self, Localmetric: Localmetric, ClickUp: ClickUp) -> None:
        self.__ClickUp = ClickUp
        self.__Localmetric = Localmetric

        self.__ClientsOwners: dict[str, list[str]] = Localmetric.getClientsOwners()
        self.__ClientExceptions: set[str] = { 'Ford Sin respuesta', 'Ford Portugal Sin Respuesta', 'Cafe Europa', 'Milwakee', 'Robata', 'Monster Sushi' }
        
        self.__ClientsFoldersID: dict[str, str] = ClickUp.Folders.getFoldersInfo(ClickUp.getSpacesInfo()['Clientes'])