import re
import time

from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi


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
        registration = Registration(
            login=login,
            password=password,
            email=email
        )
        response = self.dm_account_api.account_api.post_v1_account(registration=registration)
        assert response.status_code == 201, f'Пользователь не был создан: {response.text}'
        start_time = time.time()
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        end_time = time.time()
        assert end_time - start_time < 5, 'Время ожидания активации превышено'
        assert response.status_code == 200, "Письма не были получены"
        token = self.get_activation_token_by_login(login=login, response=response)
        assert token, f'Не найден токен активации для {login}'
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        return response

    def auth_client(
        self,
        login: str,
        password: str
    ):
        response= self.user_login(login=login, password=password)
        token = {
        'x-dm-auth-token': response.headers['x-dm-auth-token']
        }
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)

    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True
    ):
        login_credentials = LoginCredentials(
            login=login,
            password=password,
            remember_me=remember_me
        )
        response= self.dm_account_api.login_api.post_v1_account_login(
            login_credentials=login_credentials
        )
        assert response.headers.get('X-Dm-Auth-Token'), 'Токен авторизации не получен'
        return response


    def change_mail(
            self,
            login: str,
            password: str,
            new_email: str
    ):
        # Запрос на смену email
        change_email = ChangeEmail(
            login=login,
            password=password,
            email=new_email
        )
        response = self.dm_account_api.account_api.put_v1_account_email(change_email=change_email)
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, "Письма не были получены после смены email"

        # Подтверждение нового email
        new_token = self.get_activation_token_by_login(login=login, response=response)
        assert new_token, 'Не найден токен активации для нового email'
        self.dm_account_api.account_api.put_v1_account_token(token=new_token)

    def change_password(
            self,
            login: str,
            password: str,
            new_password: str,
            email: str
    ):
        # Получаем токен авторизации
        response = self.user_login(login=login, password=password)
        auth_token = response.headers['x-dm-auth-token']
        assert auth_token, 'Токен авторизации не получен'

        # Инициируем сброс пароля
        response = self.dm_account_api.account_api.post_v1_account_password(
            reset_password=ResetPassword(
                login=login,
                email=email
            )
        )
        assert response.status_code == 200, f"Не удалось инициировать сброс пароля: {response.text}"

        # Получаем токен сброса из письма
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, "Письма не были получены после смены email"
        token = self.get_activation_token_by_login(login=login, response=response)
        assert token, 'Не найден токен активации для нового email'

        new_password = password + "1"
        change_password = ChangePassword(
            login=login,
            token=token,
            oldPassword=password,
            newPassword=new_password
        )
        response = self.dm_account_api.account_api.put_v1_account_password(
            change_password=change_password,
            token=auth_token
        )
        return new_password

    def delete_login(
            self,
            **kwargs
    ):
        headers = {}
        token = kwargs.get('token')
        if token:
            headers = {
                "X-Dm-Auth-Token": token
            }

        response = self.dm_account_api.login_api.delete_v1_account_login(headers=headers)
        return response

    def delete_login_all(
            self,
            **kwargs
            ):
        headers = {}
        token = kwargs.get('token')
        if token:
            headers = {
                "X-Dm-Auth-Token": token
            }

        response = self.dm_account_api.login_api.delete_v1_account_login_all(headers=headers)
        return response

    @staticmethod
    def get_activation_token_by_login(
            login: str,
            response
    ):
        items = response.json()['items']
        for item in items:
            body = item['Content']['Body']
            if login in body:
                # Поиск UUID в тексте
                match = re.search(r'[a-f0-9\-]{36}', body)
                if match:
                    return match.group(0)
        return None
