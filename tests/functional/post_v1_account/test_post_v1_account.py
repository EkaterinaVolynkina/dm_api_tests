import allure
import pytest

from checkers.http_checkers import check_status_code_http
from dm_api_account.models.registration import Registration

@allure.suite('Тесты на проверку метода POST v1/account')
@allure.sub_suite('Позитивные тесты')
class TestPostV1Account:
    @allure.title('Проверка регистрации нового пользователя')
    def test_post_v1_account(
            self,
            account_helper,
            prepare_user
            ):

        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email
        account_helper.register_new_user(login=login, password=password, email=email)


    @allure.sub_suite('Негативные тесты')
    @pytest.mark.parametrize('login, email, password, expected_status_code', [
        ('user1', 'email@mail.ru', '123', 400),
        ('user2', 'emailmail.ru', 'Qwerty123!', 400),
        ('k', 'email@mail.ru', 'Qwerty123!', 400)
    ])

    @allure.title('Проверка 3 негативных сценариев')
    @allure.title('Проверка 3 негативных сценариев')
    def test_post_v1_account_negative(
            self,
            account_helper,
            login,
            email,
            password,
            expected_status_code
            ):
        with check_status_code_http(expected_status_code):
            account_helper.register_new_user(login=login, password=password, email=email)