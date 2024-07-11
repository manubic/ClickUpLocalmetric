from lib.clickUp.ClickUp import ClickUp
from lib.other.LocalmetricManager import Localmetric



class __BaseManager:
    def __init__(self, Localmetric: Localmetric, ClickUp: ClickUp) -> None:
        self._ClickUp = ClickUp
        self._Localmetric = Localmetric

        self._ClientsOwners: dict[str, list[str]] = Localmetric.getClientsOwners()
        self._ClientExceptions: set[str] = { 'Ford Sin respuesta', 'Ford Portugal Sin Respuesta', 'Cafe Europa', 'Milwakee', 'Robata', 'Monster Sushi' }
        
        self._ClientsFoldersID: dict[str, str] = ClickUp.Folders.getFoldersInfo(ClickUp.Spaces.getSpacesInfo()['Clientes'])