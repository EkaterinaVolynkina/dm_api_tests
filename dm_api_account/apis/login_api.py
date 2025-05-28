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
