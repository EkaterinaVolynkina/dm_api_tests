import re
import time
from json import loads
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi
from retrying import retry


def retry_if_result_none(
        result
        ):
    """Return True if we should retry (in this case when result is None), False otherwise"""
    return result is None
def retrier(
        function
        ):
    def wrapper(
            *args,
            **kwargs
            ):
        token = None
        count = 0
        while token is None:
            print(f'Попытка получения токена №{count}')
            token = function(*args, **kwargs)
            count +=1
            if count == 5:
                raise AssertionError('Превышено количество попыток получения активационного токена!')
            if token:
                return token
            time.sleep(1)

    return wrapper
class AccountHelper:
    def __init__(
            self,
            dm_account_api: DMApiAccount,
            mailhog: MailHogApi
    ):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def register_new_user(
            self,
            login: str,
            password: str,
            email: str
    ):
        json_data = {
            'login': login,
            'password': password,
            'email': email,
        }
        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, f'Пользователь не был создан: {response.text}'
        token = self.get_activation_token_by_login(login=login)
        assert token, f'Не найден токен активации для {login}'
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, 'Активация пользователя не удалась'
        return response

    def user_login(
            self,
            login: str,
            password: str
    ):
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': True,
        }
        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == 200, 'Не удалось авторизоваться после активации'
        token = response.headers.get('X-Dm-Auth-Token')
        assert token, 'Токен авторизации не получен'
        return token

    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_activation_token_by_login(
            self,
            login
    ):
        token = None
        time.sleep(3)
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, "Письма не были получены"
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
        return token
