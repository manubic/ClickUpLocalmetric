import requests
from lib.clickUp.api.__base import __Base



class Lists(__Base):
    def __init__(self, config) -> None:
        super().__init__(config)
    
    def getListsInfo(self, folderID: str) -> dict[str, str]:
        return {
            _list['name']: _list['id']
            for _list in requests.get(
                    f'https://api.clickup.com/api/v2/folder/{folderID}/list',
                    headers = self._headers, params = { 'archived': 'false' }
                ).json()['lists']
            }
    
    def createLists(self, newName: str, folderID: str, exceptions: set[str]) -> list[str]:
        _newHeaders = { 'Content-Type': 'application/json' }
        _newHeaders.update(self._headers)
        _oldLists = self.getListsInfo(folderID)
        
        return requests.post(
                f'https://api.clickup.com/api/v2/folder/{folderID}/list',
                headers = _newHeaders,
                json = { "name": newName }
            ).json()['id'] if newName not in _oldLists and newName not in exceptions else ''
            