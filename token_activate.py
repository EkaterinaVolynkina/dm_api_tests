import pprint

import requests

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