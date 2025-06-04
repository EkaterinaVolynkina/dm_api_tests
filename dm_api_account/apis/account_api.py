import requests

from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
from dm_api_account.models.user_details_envelope import UserDetailsEnvelope
from dm_api_account.models.user_envelope import UserEnvelope
from restclient.client import RestClient


class AccountApi(RestClient):
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

    def post_v1_account_password(
            self,
            reset_password: ResetPassword
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
            json=reset_password.model_dump(exclude_none=True, by_alias=True)
        )

    def get_v1_account(
            self,
            validate_response=True,
            **kwargs
    ):
        """
        Get current user
        """
        response = self.get(
            path='/v1/account',
            **kwargs
        )
        parsed = UserDetailsEnvelope.model_validate_json(response.text)
        return response.status_code, parsed

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

        response = requests.put(
            url=f'{self.host}/v1/account/password',
            json=change_password.model_dump(by_alias=True),
            headers=headers
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    def put_v1_account_email(
            self,
            change_email: ChangeEmail,
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
            json=change_email.model_dump(exclude_none=True, by_alias=True)
        )

