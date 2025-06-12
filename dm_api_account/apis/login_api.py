import requests

from dm_api_account.models.general_error import GeneralError
from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.user_envelope import UserEnvelope
from restclient.client import RestClient


class LoginApi(RestClient):

    def post_v1_account_login(
            self,
            login_credentials: LoginCredentials,
            validate_response=False
    ):
        response = self.post(
            path=f'/v1/account/login',
            json=login_credentials.model_dump(exclude_none=True, by_alias=True)
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    def delete_v1_account_login(
            self,
            validate_response=False,
            **kwargs
    ):

        response = self.delete(
            path='/v1/account/login'
        )
        if validate_response:
            return GeneralError(**response.json())
        return response

    def delete_v1_account_login_all(
            self,
            validate_response=False,
            **kwargs
            ):


        response = self.delete(
            path='/v1/account/login/all'
        )
        if validate_response:
            return GeneralError(**response.json())
        return response