import token

import requests

from restclient.client import RestClient


class LoginApi(RestClient):

    def post_v1_account_login(
            self,
            json_data
        ):
        """
        Authenticate via credentials
        :param json_data:
        :return:
        """
        response = self.post(
            path=f'/v1/account/login',
            json=json_data
        )
        return response

    def delete_v1_account_login(
            self,
            **kwargs
    ):
        """
        Delete current user session
        """
        token = kwargs.get('token')

        headers = {
            'accept': '*/*',
        }

        if token:
            headers['X-Dm-Auth-Token'] = token

        return requests.delete(
            url=f'{self.host}/v1/account/login',
            headers=headers
        )

    def delete_v1_account_login_all(
            self,
            token: str | None = None
            ):
        headers = {}
        if token:
            headers = {
                "X-Dm-Auth-Token": 'token'
            }

        response = self.delete_v1_account_login(
            url=f'{self.host}/v1/account/login/all',
            headers=headers)
        return response
