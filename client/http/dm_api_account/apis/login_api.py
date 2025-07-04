from client.http.dm_api_account.models.login_credentials import LoginCredentials
from client.http.dm_api_account.models.user_envelope import UserEnvelope
from packages.restclient.client import RestClient


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
            **kwargs
    ):

        response = self.delete(
            path='/v1/account/login',
            **kwargs
        )
        return response

    def delete_v1_account_login_all(
            self,
            **kwargs
    ):

        response = self.delete(
            path='/v1/account/login/all',
            **kwargs
        )
        return response
