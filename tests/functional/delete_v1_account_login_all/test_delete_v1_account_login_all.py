import allure

from checkers.http_checkers import check_status_code_http


@allure.suite('Тесты на проверку метода DELETE v1/account/login/all')
@allure.sub_suite('Удаление всех сессий пользователя')
class TestDeleteV1AccountLoginAll:
    @allure.title("Удаление всех сессий авторизованного пользователя")
    def test_delete_v1_account_login_all(self, auth_account_helper):
        with check_status_code_http():
            auth_account_helper.delete_login_all()

    @allure.title("Удаление всех сессий неавторизованного пользователя")
    def test_delete_v1_account_login_negative_all(self, account_helper):
        with check_status_code_http(401, 'User must be authenticated'):
            account_helper.delete_login_all()
