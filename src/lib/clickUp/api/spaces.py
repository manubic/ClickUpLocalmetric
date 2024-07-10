import requests
from lib.clickUp.api.__base import __Base



class Spaces(__Base):
    def __init__(self, config) -> None:
        super.__init__(config)
    
    def getSpacesInfo(self) -> dict[str, str]:
        return {
            _space['name']: _space['id']
            for _space in requests.get(
                f'https://api.clickup.com/api/v2/team/{self._teamID}/space',
                headers = self.__headers, params = { 'archived': 'false' }
            ).json()['spaces']
        }