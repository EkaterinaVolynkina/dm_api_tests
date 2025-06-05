import requests
from restclient.client import RestClient


class AccountApi(RestClient):
    def post_v1_account(
            self,
            json_data
            ):
        """
        Register new user
        :param json_data:
        :return:
        """
        response = self.post(
            path=f'/v1/account',
            json=json_data
        )
        return response

    def post_v1_account_password(
            self,
            json_data
    ):
        """
        Reset registered user password
        """

        headers = {
            'accept': 'text/plain',
            'Content-Type': 'application/json',
        }
        return requests.post(
            url=f'{self.host}/v1/account/password',
            headers=headers,
            json=json_data
        )

    def get_v1_account(
            self,
            **kwargs
            ):
        """
        Get current user
        :return:
        """
        response = self.get(
            path=f'/v1/account',
            **kwargs
        )
        return response
    def put_v1_account_token(
            self,
            token
            ):
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
        return response

    def put_v1_account_password(
            self,
            json_data,
            **kwargs
    ):
        """
        Change registered user password
        """
        token = kwargs.get('token')  # достаем токен из kwargs

        headers = {
            'accept': 'text/plain',
            'Content-Type': 'application/json',
        }

        if token:
            headers['X-Dm-Auth-Token'] = token  # добавляем токен, если есть

        return requests.put(
            url=f'{self.host}/v1/account/password',
            headers=headers,
            json=json_data
        )

    def put_v1_account_email(
            self,
            json_data,
            **kwargs
    ):
        """
        Change registered user email
        """
        headers = {
            'accept': 'text/plain',
            'Content-Type': 'application/json',
        }

        return requests.put(
            url=f'{self.host}/v1/account/email',
            headers=kwargs.get('token'),
            json=json_data
        )

