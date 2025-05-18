import requests


def test_post_v1_account():
    # Регистрация пользователя
    login = 'katya_1_2365_45',
    password = '123456789'
    email = f'{login}@mail.ru'

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account', json=json_data)
    print(response.status_code)
    print(response.text)

    # Получить письма из почтового адреса

    params = {
        'limit': '50',
    }

    response = requests.get('http://5.63.153.31:5025/api/v2/messages', params=params)
    print(response.status_code)
    print(response.text)

    # Получить активационный токен

    # Активация пользователя

    headers = {
        'accept': 'text/plain',
    }

    response = requests.put('http://5.63.153.31:5051/v1/account/2ca2c0bd-324d-4b8b-9711-07ce6221a8cd', headers=headers)
    print(response.status_code)
    print(response.text)
    # Авторизоваться

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account/login', headers=headers, json=json_data)
    print(response.status_code)
    print(response.text)
