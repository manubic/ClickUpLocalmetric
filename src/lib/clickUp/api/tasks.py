import requests
from lib.clickUp.api.__base import __Base



class Tasks(__Base):
    def __init__(self, config) -> None:
        super().__init__(config)
    
    def createOrUploadTaskInList(self, name: str, description: str, asignedUsers: set[str], listId: str,
                         settings: dict[str, str | list[str]] = {}, method: list[str] = ['get']) -> list[str]:

        _newHeaders = { 'Content-Type': 'application/json' }
        _newHeaders.update(self.__headers)

        if method[0] == 'put':
            for field in settings['custom_fields']:
                self.updateTasksFields(
                    method[1], field['id'],
                    { key: field[key] for key in field if key != 'id' } 
                )
            return

        _body = {
            "name": name, "description": description,
            "assignees": [self._usersId[_name] for _name in self._usersId if _name in asignedUsers], 
        }
        _body.update(settings)

        requests.post(
            f'https://api.clickup.com/api/v2/list/{listId}/task',
            headers = _newHeaders, json = _body,
            params = { 'custom_task_ids': 'true', 'team_id': self._teamID }).json()
    
    def getTasksFields(self, listID: str) -> dict[str, dict[str, str]]:
        _tasks = requests.get(
                f'https://api.clickup.com/api/v2/list/{listID}/task',
                headers = self.__headers,
            ).json()

        return {
            task['custom_fields'][6]['value']: {'id': task['id'], **{
                taskValue['name']: taskValue['value']
                for taskValue in task['custom_fields'] 
                if taskValue['name'] != 'id' and 'value' in taskValue
            }}
            for task in _tasks['tasks'] 
        } if 'tasks' in _tasks and len(_tasks['tasks']) > 0 else {}
    
    def updateTasksFields(self, taskId: str, fieldId: str, settings: dict[str, str]) -> None:
        _newHeaders = { 'Content-Type': 'application/json' }
        _newHeaders.update(self.__headers)
        requests.post(
            f'https://api.clickup.com/api/v2/task/{taskId}/field/{fieldId}',
            headers = _newHeaders, params = { 'custom_task_ids': 'true', 'team_id': self._teamID },
            json = settings,
        )
    
    def updateTask(self, taskId: str, settings: dict[str, str]) -> None:
        _newHeaders = { 'Content-Type': 'application/json' }
        _newHeaders.update(self.__headers)
        requests.put(
            f'https://api.clickup.com/api/v2/task/{taskId}',
            json = settings, headers = _newHeaders, params = { 'custom_task_ids': 'true', 'team_id': self._teamID }
        )
    
    def deleteTaskOfList(self, taskId: str) -> None:
        _newHeaders = { 'Content-Type': 'application/json' }
        _newHeaders.update(self.__headers)
        
        requests.delete(
            f'https://api.clickup.com/api/v2/task/{taskId}',
            headers = _newHeaders,
            params = { 'custom_task_ids': 'true', 'team_id': self._teamID }
        )