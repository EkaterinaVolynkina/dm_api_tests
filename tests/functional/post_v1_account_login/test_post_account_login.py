import allure

from checkers.post_v1_account_login import PostV1Account

@allure.suite('Тесты на проверку метода POST v1/account/login')
@allure.sub_suite('Позитивные тесты')
class TestPostV1AccountLogin:
    @allure.title('Проверка регистрации аутентификации пользователя')
    def test_post_v1_account_login(
            self,
            account_helper,
            prepare_user
            ):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email
        account_helper.register_new_user(login=login, password=password, email=email)
        response = account_helper.user_login(login=login, password=password, validate_response=True)
        PostV1Account.check_response_values(response)



