import requests
from lib.clickUp.api.__base import __Base



class Folders(__Base):
    def __init__(self, config) -> None:
        super().__init__(config)
    
    def getFoldersInfo(self, spaceID: str) -> dict[str, str]:
        return {
            _folder['name']: _folder['id']
            for _folder in requests.get(
                f'https://api.clickup.com/api/v2/space/{spaceID}/folder',
                headers = self._headers, params = { 'archived': 'false' }
            ).json()['folders']
        }