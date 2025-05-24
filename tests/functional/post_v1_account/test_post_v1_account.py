from dm_api_account.apis.account_api import AccountApi
from data import USER, EMAIL, PASSWORD
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            #ensure_ascii=True,
            #sort_keys=True
        )
    ]
)

def test_post_v1_account():
    # Инициализация клиентов
    account_api = AccountApi(host='http://5.63.153.31:5051')

    login = USER
    password = PASSWORD
    email = EMAIL

    # Регистрация пользователя
    response = account_api.post_v1_account(json_data={
        'login': login,
        'email': email,
        'password': password,
    })
    assert response.status_code == 201, f'Пользователь не был создан: {response.text}'

