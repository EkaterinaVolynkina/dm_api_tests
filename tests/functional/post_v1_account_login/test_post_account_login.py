from json import loads
from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi
from data import generate_user
import structlog
from restclient.configuration import Configuration as DmApiConfiguration
from restclient.configuration import Configuration as MailHogConfiguration

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
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    mailhog_configuration = MailHogConfiguration(host='http://5.63.153.31:5025')

    account_api = AccountApi(configuration=dm_api_configuration)
    login_api = LoginApi(configuration=dm_api_configuration)
    mailhog_api = MailhogApi(configuration=mailhog_configuration)

    login, email, password = generate_user()

    #  Регистрация пользователя
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

def get_activation_token_by_login(login, response):
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        if user_data['Login'] == login:
            return user_data['ConfirmationLinkUrl'].split('/')[-1]
    return None
