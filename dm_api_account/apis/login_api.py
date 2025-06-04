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
        """
        Authenticate via credentials

        """
        response = self.post(
            path=f'/v1/account/login',
            json=login_credentials.model_dump(exclude_none=True, by_alias=True)
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    def delete_v1_account_login(
            self,
            token
            ):
        headers = {
            'accept': '*/*',
            'X-Dm-Auth-Token': token
        }
        return requests.delete(
            url=f'{self.host}/v1/account/login',
            headers=headers
        )

    def delete_v1_account_login_all(
            self,
            token
    ):
        """
        Logout from every device
        """

        headers = {
            'accept': '*/*',
            'X-Dm-Auth-Token': token
        }

        return requests.delete(
            url=f'{self.host}/v1/account/login/all',
            headers=headers
        )
