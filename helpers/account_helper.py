import re
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
        json_data = {
            'login': login,
            'password': password,
            'email': email,
        }
        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, f'Пользователь не был создан: {response.text}'
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, "Письма не были получены"
        token = self.get_activation_token_by_login(login=login, response=response)
        assert token, f'Не найден токен активации для {login}'
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, 'Активация пользователя не удалась'
        return response

    def auth_client(
            self,
            login: str,
            password: str
    ):
        response = self.dm_account_api.login_api.post_v1_account_login(
            json_data={
                'login': login,
                'password': password
            }
        )
        token = {
            'x-dm-auth-token': response.headers['x-dm-auth-token']
        }
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)

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
        token_headers = {
            'X-Dm-Auth-Token': response.headers.get('X-Dm-Auth-Token')
        }
        assert token_headers, 'Токен авторизации не получен'
        return token_headers


    def change_mail(
            self,
            login: str,
            password: str,
            new_email: str
    ):
        # Запрос на смену email
        json_data = {
            'login': login,
            'password': password,
            'email': new_email,
        }
        response = self.dm_account_api.account_api.put_v1_account_email(json_data=json_data)
        assert response.status_code == 200, f'Не удалось отправить запрос на смену email: {response.text}'

        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, "Письма не были получены после смены email"

        # Подтверждение нового email
        new_token = self.get_activation_token_by_login(login=login, response=response)
        assert new_token, 'Не найден токен активации для нового email'
        response = self.dm_account_api.account_api.put_v1_account_token(token=new_token)
        assert response.status_code == 200, 'Подтверждение нового email не удалось'


    def change_password(
            self,
            login: str,
            password: str,
            email: str
        ):
        # Получаем токен авторизации
        response = self.dm_account_api.login_api.post_v1_account_login(
            json_data={
                "login": login,
                "password": password
            }
        )
        token = response.headers.get('X-Dm-Auth-Token')
        assert token, 'Токен авторизации не получен'


        # Инициируем сброс пароля
        response = self.dm_account_api.account_api.post_v1_account_password(
            json_data={
                "login": login,
                "email": email
            }
        )
        assert response.status_code == 200, f"Не удалось инициировать сброс пароля: {response.text}"

        # Получаем токен сброса из письма
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, "Письма не были получены после смены email"
        reset_token = self.get_activation_token_by_login(login=login, response=response)
        assert reset_token, 'Не найден токен активации для нового email'

        # Меняем пароль
        new_password = password + "1"
        json_data = {
            "login": login,
            "token": reset_token,
            "oldPassword": password,
            "newPassword": new_password
        }
        response = self.dm_account_api.account_api.put_v1_account_password(
            json_data=json_data,
            token=token
        )
        assert response.status_code == 200, f"Не удалось сменить пароль: {response.text}"

        return new_password

    def delete_login(
            self,
            login: str,
            password: str,
            email: str
            ):
        # Регистрируем пользователя
        json_data = {
            'login': login,
            'password': password,
            'email': email,
        }
        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, f'Пользователь не был создан: {response.text}'

        # Получаем письма с Mailhog и токен активации
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, "Письма не были получены"
        token = self.get_activation_token_by_login(login=login, response=response)
        assert token, f'Не найден токен активации для {login}'

        # Активируем пользователя
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, 'Активация пользователя не удалась'

        # Логинимся и получаем токен
        json_login = {
            'login': login,
            'password': password,
        }
        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_login)
        assert response.status_code == 200, f'Ошибка при логине: {response.text}'
        token = response.headers.get('X-Dm-Auth-Token')
        assert token, 'Токен авторизации не получен'

        # Выходим из аккаунта
        response = self.dm_account_api.login_api.delete_v1_account_login(token=token)
        assert response.status_code == 204, f"Не удалось выйти из аккаунта: {response.text}"


    def delete_login_all(
            self,
            login: str,
            password: str,
            email: str
    ):
        # Регистрируем пользователя
        json_data = {
            'login': login,
            'password': password,
            'email': email,
        }
        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, f'Пользователь не был создан: {response.text}'

        # Получаем письма с Mailhog и токен активации
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, "Письма не были получены"
        token = self.get_activation_token_by_login(login=login, response=response)
        assert token, f'Не найден токен активации для {login}'

        # Активируем пользователя
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, 'Активация пользователя не удалась'

        # Логинимся и получаем токен
        json_login = {
            'login': login,
            'password': password,
        }
        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_login)
        assert response.status_code == 200, f'Ошибка при логине: {response.text}'
        token = response.headers.get('X-Dm-Auth-Token')
        assert token, 'Токен авторизации не получен'

        # Выходим из аккаунта
        response = self.dm_account_api.login_api.delete_v1_account_login_all(token=token)
        assert response.status_code == 204, f"Не удалось выйти из всех аккаунтов: {response.text}"
        print(response.status_code)
        print(token)

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
