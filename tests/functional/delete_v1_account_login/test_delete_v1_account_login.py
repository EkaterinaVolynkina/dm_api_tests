import allure

from checkers.http_checkers import check_status_code_http

@allure.suite('Тесты на проверку метода DELETE v1/account/login')
@allure.sub_suite('Удаление текущей сессии пользователя')
class TestDeleteV1AccountLogin:
    @allure.title('Удаление текущей сессии авторизованного пользователя')
    def test_delete_v1_account_login(self,auth_account_helper):
        with check_status_code_http():
            auth_account_helper.delete_login()

    @allure.title('Удаление текущей сессии неавторизованного пользователя')
    def test_delete_v1_account_login_negative(self, account_helper):
        with check_status_code_http(401, 'User must be authenticated'):
            account_helper.delete_login()

