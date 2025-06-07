import requests

from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.user_envelope import UserEnvelope
from restclient.client import RestClient


class LoginApi(RestClient):

    def post_v1_account_login(
            self,
            login_credentials: LoginCredentials,
            validate_response=True
    ):
        response = self.post(
            path=f'/v1/account/login',
            json=login_credentials.model_dump(exclude_none=True, by_alias=True)
        )
        return response

    def delete_v1_account_login(
            self,
            **kwargs
            ):
        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json',
        }
        return self.delete(
            path=f'/v1/account/login',
            headers=kwargs.get('token')
        )

    def delete_v1_account_login_all(
            self,
            **kwargs
    ):
        """
        Logout from every device
        """

        headers = {
            'accept': '*/*',
            'Content-Type': 'application/json',
        }

        return self.delete(
            path=f'/v1/account/login/all',
            headers=kwargs.get('token')
        )
