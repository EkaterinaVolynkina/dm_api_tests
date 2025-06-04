import uuid


def test_put_v1_account_email(
        account_helper,
        prepare_user
        ):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    unique_suffix = uuid.uuid4().hex[:6]
    new_login = f'{login}_{unique_suffix}'

    new_email = f'{new_login}@mail.ru'
    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)
    account_helper.change_mail(login=login, password=password, new_email=new_email)
    account_helper.user_login(login=login, password=password)
