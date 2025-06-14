
import allure

from checkers.get_v1_account import GetV1Account

from checkers.http_checkers import check_status_code_http


@allure.suite('Тесты на проверку метода GET v1/account')
@allure.sub_suite('Получение данных текущего пользователя')
class TestGetV1Account:
    @allure.sub_suite('Позитивные тесты')
    @allure.title('Получение данных авторизованного пользователя')
    def test_get_v1_account_auth(self, auth_account_helper):
        with check_status_code_http():
            response = auth_account_helper.dm_account_api.account_api.get_v1_account(validate_response=True)
        GetV1Account.check_response_soft(response)
        GetV1Account.check_response_value(response)



    @allure.sub_suite('Негативные тесты')
    @allure.title('Получение данных неавторизованного пользователя')
    def test_get_v1_account_no_auth(self, account_helper):
        with check_status_code_http(401, 'User must be authenticated'):
            account_helper.dm_account_api.account_api.get_v1_account()

