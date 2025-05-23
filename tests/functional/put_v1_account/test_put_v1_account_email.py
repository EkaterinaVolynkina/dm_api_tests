from json import loads
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

    login = 'katya_1_2365_163'
    new_login = 'katya_1_2365_164'
    password = '123456789'
    email = f'{login}@mail.ru'
    new_email = f'{new_login}@mail.ru'

    # Регистрация пользователя
    response = account_api.post_v1_account(json_data={
        'login': login,
        'email': email,
        'password': password,
    })
    assert response.status_code == 201, f'Пользователь не был создан: {response.text}'

    # Получение токена активации из почты
    response = mailhog_api.get_api_v2_messages()
    token = get_activation_token_by_login(login, response)
    assert token, f'Не найден токен активации для {login}'

    # Активация пользователя
    response = account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, 'Активация пользователя не удалась'

    # Авторизация
    response = login_api.post_v1_account_login(json_data={
        'login': login,
        'password': password,
        })
    assert response.status_code == 200, 'Не удалось авторизоваться после активации'


    # Отправка запроса на смену email
    json_data = {
        'login': login,
        'password': password,
        'email': new_email,
    }
    response = account_api.put_v1_account_email(json_data=json_data, headers=token)
    assert response.status_code == 200, f'Не удалось отправить запрос на смену email: {response.text}'

    # Проверка, что вход с новым логином/email не работает без активации
    response = login_api.post_v1_account_login(
        json_data={
            'login': login,
            'password': password,
        }
    )
    assert response.status_code == 403, 'Вход по новому email не работает'

    # Получение нового письма с подтверждением email
    response = mailhog_api.get_api_v2_messages()
    new_token = get_activation_token_by_login(login, response)
    assert new_token, f'Не найден токен подтверждения для нового email: {new_email}'

    # Активация нового email

    response = account_api.put_v1_account_token(token=new_token)
    assert response.status_code == 200, 'Подтверждение нового email не удалось'

 # Авторизация с новым email
    response = login_api.post_v1_account_login(json_data={
        'login': login,
        'password': password,
        })
    assert response.status_code == 200, 'Не удалось авторизоваться после активации'

def get_activation_token_by_login(login, response):
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        if user_data['Login'] == login:
            return user_data['ConfirmationLinkUrl'].split('/')[-1]
    return None
