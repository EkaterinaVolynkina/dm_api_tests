import pprint

import requests

url = 'http://5.63.153.31:5051/v1/account/4fa73809-7dea-44e8-b3ba-071f06ea796e'
headers = {
    'accept': 'text/plain'
}
response = requests.put(
  url=url,
  headers=headers
)
print(response.status_code)
pprint.pprint(response.json())
response_json = response.json()
print(response_json['resource']['rating']['quality'])