import pprint
import  requests

url = 'http://5.63.153.31:5051/v1/account'
headers = {
    'accept': '*/*',
    'Content-Type': 'application/json'
}
json = {
    'login': 'katya_1_2365_7',
    'email': 'katya_1_2365_7@mail.ru',
    'password': '123456789'
}
response = requests.post(
    url=url,
    headers=headers,
    json=json
)
print(response.status_code)
