import requests



class ClickUp:
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
    
    def getTasksIdField(self, listID: str) -> dict[str, str]:
        _tasks = requests.get(
                f'https://api.clickup.com/api/v2/list/{listID}/task',
                headers = self.__headers,
            ).json()
        return {
            task['custom_fields'][6]['value']: task['id']
            for task in _tasks['tasks'] 
        } if 'tasks' in _tasks and len(_tasks['tasks']) > 0 else {}
    
    def getFieldsInfo(self, listID: str) -> dict[str, str]:
        _newHeaders = { 'Content-Type': 'application/json' }
        _newHeaders.update(self.__headers)
        return {
            _field['name']: _field['id']
            for _field in requests.get(
                f'https://api.clickup.com/api/v2/list/{listID}/field',
                headers = _newHeaders
            ).json()['fields']
        }
    
    def getListsInfo(self, folderID: str) -> dict[str, str]:
        return {
            _list['name']: _list['id']
            for _list in requests.get(
                    f'https://api.clickup.com/api/v2/folder/{folderID}/list',
                    headers = self.__headers, params = { 'archived': 'false' }
                ).json()['lists']
            }
    
    def getSpacesInfo(self) -> dict[str, str]:
        return {
            _space['name']: _space['id']
            for _space in requests.get(
                f'https://api.clickup.com/api/v2/team/{self._teamID}/space',
                headers = self.__headers, params = { 'archived': 'false' }
            ).json()['spaces']
        }
    
    def getFoldersInfo(self, spaceID: str) -> dict[str, str]:
        return {
            _folder['name']: _folder['id']
            for _folder in requests.get(
                f'https://api.clickup.com/api/v2/space/{spaceID}/folder',
                headers = self.__headers, params = { 'archived': 'false' }
            ).json()['folders']
        }
    
    def createLists(self, newNames: list[str], folderID: str) -> list[str]:
        _newHeaders = { 'Content-Type': 'application/json' }
        _newHeaders.update(self.__headers)
        _oldLists = self.getListsInfo(folderID)
        
        return [
            requests.post(
                f'https://api.clickup.com/api/v2/folder/{folderID}/list',
                headers = _newHeaders,
                json = { "name": newName }
            ).json()['id']
            for newName in newNames
            if newName not in _oldLists
        ]
    
    def createOrUploadTaskInList(self, name: str, description: str, asignedUsers: set[str], listId: str,
                         settings: dict[str, str | list[str]] = {}, method: list[str] = ['get']) -> list[str]:

        _newHeaders = { 'Content-Type': 'application/json' }
        _newHeaders.update(self.__headers)
        if method[1] == 'get':
            _urlSettings = [requests.post, f'https://api.clickup.com/api/v2/list/{listId}/task']
        else:
            _urlSettings = [requests.put, f'https://api.clickup.com/api/v2/task/{method[1]}']
        
        _body = {
            "name": name, "description": description,
            "assignees": [self._usersId[_name] for _name in self._usersId if _name in asignedUsers], 
        }
        _body.update(settings)
        result = _urlSettings[0](
            _urlSettings[1],
            headers = _newHeaders, json = _body,
            params = {"custom_task_ids": "true", "team_id": self._teamID}).json()
        print(result['id'])
    
    def deleteTaskOfList(self, taskId: str) -> None:
        _newHeaders = { 'Content-Type': 'application/json' }
        _newHeaders.update(self.__headers)
        
        requests.delete(
            f'https://api.clickup.com/api/v2/task/{taskId}',
            headers = _newHeaders,
            params = {"custom_task_ids": "true", "team_id": self._teamID}
        )