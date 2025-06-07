import pytest

from checkers.http_checkers import check_status_code_http
from dm_api_account.models.registration import Registration


def test_post_v1_account(
        account_helper,
        prepare_user
        ):

    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    account_helper.register_new_user(login=login, password=password, email=email)


@pytest.mark.parametrize('login, email, password, expected_status_code', [
    ('user1', 'email@mail.ru', '123', 400),
    ('user2', 'emailmail.ru', 'Qwerty123!', 400),
    ('k', 'email@mail.ru', 'Qwerty123!', 400)
])
def test_post_v1_account_negative(account_helper, login, email, password, expected_status_code):
    with check_status_code_http(expected_status_code):
        account_helper.register_new_user(login=login, password=password, email=email)