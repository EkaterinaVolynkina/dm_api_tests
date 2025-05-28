import uuid
from data import generate_user
def test_put_v1_account_email(account_helper, account_api):
       # Генерируем уникальный логин
    login, email, password = generate_user()
    unique_suffix = uuid.uuid4().hex[:6]
    new_login = f'{login}_{unique_suffix}'

    new_email = f'{new_login}@mail.ru'
    # Регистрируем нового пользователя

    account_helper.register_new_user(login=login, password=password, email=email)

    # Авторизация и получение токена
    account_helper.user_login(login=login, password=password)

    # Запрос на смену email
    # Обновляем список писем после запроса
   
    account_helper.change_mail(login=login, password=password, new_email=new_email)

    # Авторизация с новым email
    account_helper.user_login(login=login, password=password)
