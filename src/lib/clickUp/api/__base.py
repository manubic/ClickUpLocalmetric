import requests



class __Base:
    def __init__(self, config) -> None:
        self.__headers = {
            'Authorization': config.ClickUpApiKey
        }
        self._teamID = requests.get('https://api.clickup.com/api/v2/team', headers=self.__headers).json()['teams'][0]['id']
        self._usersId = self.__getUsersId()
    
    def __getUsersId(self) -> dict[str, int]:
        return {
            _user['user']['username']: _user['user']['id']
            for _user in requests.get(
                'https://api.clickup.com/api/v2/team',
                headers = self.__headers
            ).json()['teams'][0]['members']
        }