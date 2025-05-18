import pprint

import requests

url = 'http://5.63.153.31:5051/v1/account/2ca2c0bd-324d-4b8b-9711-07ce6221a8cd'
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