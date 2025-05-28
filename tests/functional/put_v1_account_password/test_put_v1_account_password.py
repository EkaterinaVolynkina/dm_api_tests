def test_put_v1_account_password(
        account_helper,
        prepare_user
        ):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    # Регистрация пользователя
    account_helper.register_new_user(login=login, password=password, email=email)

    # Авторизация пользователя
    account_helper.user_login(login=login, password=password)

    # Смена пароля
    new_password = account_helper.change_password(login=login, password=password, email=email)

    # Авторизация пользователя с новым паролем
    account_helper.user_login(login=login, password=new_password)

