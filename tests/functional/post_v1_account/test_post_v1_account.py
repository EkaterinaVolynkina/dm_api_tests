from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi
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
    login_api = LoginApi(host='http://5.63.153.31:5051')
    mailhog_api = MailhogApi(host='http://5.63.153.31:5025')

    login = 'katya_1_2365_160'
    password = '123456789'
    email = f'{login}@mail.ru'

    # Регистрация пользователя
    response = account_api.post_v1_account(json_data={
        'login': login,
        'email': email,
        'password': password,
    })
    assert response.status_code == 201, f'Пользователь не был создан: {response.text}'

