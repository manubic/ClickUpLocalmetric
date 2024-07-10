import requests
from datetime import datetime

list_id = '901202812963'
url = "https://api.clickup.com/api/v2/list/" + list_id + "/task"


headers = {"Authorization": "pk_74574880_U6AXIFZ8062N2VMA4TWVQG8T26OKU8VL"}

response = requests.get(url, headers=headers)

data = response.json()
print(datetime.fromtimestamp(int(data['tasks'][0]['custom_fields'][2]['value'])/1000))
