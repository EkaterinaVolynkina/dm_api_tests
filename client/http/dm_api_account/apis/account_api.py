import allure

from client.http.dm_api_account.models.change_email import ChangeEmail
from client.http.dm_api_account.models.change_password import ChangePassword
from client.http.dm_api_account.models.registration import Registration
from client.http.dm_api_account.models.reset_password import ResetPassword
from client.http.dm_api_account.models.user_details_envelope import UserDetailsEnvelope
from client.http.dm_api_account.models.user_envelope import UserEnvelope
from packages.restclient.client import RestClient


class AccountApi(RestClient):
    @allure.step('Регистрируем нового пользователя')
    def post_v1_account(
            self,
            registration: Registration
            ):
        """
        Register new user
        :param json_data:
        :return:
        """

        response = self.post(
            path=f'/v1/account',
            json=registration.model_dump(exclude_none=True, by_alias=True)
        )

        return response

    @allure.step('Сбрасываем пароль')
    def post_v1_account_password(
            self,
            reset_password: ResetPassword,
            validate_response: bool = True,
            **kwargs
    ):
        """
        Reset registered user password
        """

        response = self.post(
            path=f'/v1/account/password',
            json=reset_password.model_dump(exclude_none=True, by_alias=True),
            **kwargs
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    @allure.step('Получаем данные пользователя')
    def get_v1_account(
            self,
            validate_response=True,
            **kwargs
    ):
        """
        Get current user
        """
        response = self.get(
            path=f'/v1/account',
            **kwargs
        )
        if validate_response:
            return UserDetailsEnvelope(**response.json())
        return response

    @allure.step('Активируем пользователя')
    def put_v1_account_token(
            self,
            token,
            validate_response=True):
        """
        Activate registered user
        :param token:
        :return:
        """
        headers = {
            'accept': 'text/plain'
        }
        response = self.put(
            path=f'/v1/account/{token}',
            headers=headers
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    @allure.step('Меняем пароль')
    def put_v1_account_password(
            self,
            change_password: ChangePassword,
            token: str = None,
            validate_response=True
    ):
        """
        Change registered user password
        """
        headers = {
            'accept': 'text/plain',
            'Content-Type': 'application/json',
        }

        if token:
            headers['X-Dm-Auth-Token'] = token

        response = self.put(
            path=f'/v1/account/password',
            json=change_password.model_dump(by_alias=True),
            headers=headers
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    @allure.step('Меняем email')
    def put_v1_account_email(
            self,
            change_email: ChangeEmail,
            validate_response: bool = True,
            **kwargs
    ):
        """
        Change registered user email
        """
        response = self.put(
            path=f'/v1/account/email',
            headers=kwargs.get('token'),
            json=change_email.model_dump(exclude_none=True, by_alias=True),
            **kwargs
        )

        if validate_response:
            return UserEnvelope(**response.json())
        return response

