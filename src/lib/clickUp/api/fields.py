import requests
from lib.clickUp.api.__base import __Base



class Fields(__Base):
    def __init__(self, config) -> None:
        super().__init__(config)
    
    def getFieldsInfo(self, listID: str) -> dict[str, str]:
        _newHeaders = { 'Content-Type': 'application/json' }
        _newHeaders.update(self._headers)
        return {
            _field['name']: _field['id']
            for _field in requests.get(
                f'https://api.clickup.com/api/v2/list/{listID}/field',
                headers = _newHeaders
            ).json()['fields']
        }