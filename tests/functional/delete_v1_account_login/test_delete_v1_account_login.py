def test_delete_v1_account_password(
        account_helper,
        prepare_user
):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    #Выходим из аккаунта
    account_helper.delete_login(login=login, password=password, email=email)


