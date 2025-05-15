import pprint
import  requests
"""
url = 'http://5.63.153.31:5051/v1/account'
headers = {
    #'accept': '*/*',
    #'Content-Type': 'application/json'
}
json = {
    'login': 'vmenshikov_test43',
    'email': 'vmenshikov_test43@mail.ru',
    'password': '123456789'
}
response = requests.post(
    url=url,
    headers=headers,
    json=json
)
print(response.status_code)
pprint.pprint(response.json())
"""

url = 'http://5.63.153.31:5051/v1/account/0914414b-43dc-4ba9-b0c4-996742430aae'
headers = {
    'accept': 'text/plain'
}
response = requests.put(
  url = url,
  headers = headers
)
print(response.status_code)
pprint.pprint(response.json())
response_json = response.json()
print(response_json['resource']['rating']['quality'])