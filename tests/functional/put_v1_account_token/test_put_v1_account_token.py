import allure


@allure.suite('Тесты на проверку метода PUT v1/account/token')
@allure.sub_suite('Активация зарегистрированного пользователя')
class TestPutV1AccountToken:
    @allure.title('Активация пользователя')
    def test_put_v1_account_token(
            self,
            account_helper,
            prepare_user
            ):

        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email
        account_helper.register_new_user(login=login, password=password, email=email)
        account_helper.user_login(login=login, password=password)
