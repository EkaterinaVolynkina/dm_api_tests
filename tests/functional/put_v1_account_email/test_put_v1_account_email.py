import uuid
from data import generate_user
def test_post_v1_account_email(account_helper, account_api):
       # Генерируем уникальный логин
    login, email, password = generate_user()
    unique_suffix = uuid.uuid4().hex[:6]
    new_login = f'{login}_{unique_suffix}'

    new_email = f'{new_login}@mail.ru'

    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)

    # Авторизация и получение токена
    token_value = account_helper.user_login(login=login, password=password)
    token = {
        'X-Dm-Auth-Token': token_value
    }
    # Запрос на смену email
    json_data = {
        'login': login,
        'password': password,
        'email': new_email,
    }
    response = account_api.account_api.put_v1_account_email(json_data=json_data, headers=token)
    assert response.status_code == 200, f'Не удалось отправить запрос на смену email: {response.text}'

    # Обновляем список писем после запроса
    response = account_helper.mailhog.mailhog_api.get_api_v2_messages()
    assert response.status_code == 200, "Письма не были получены после смены email"

    # Подтверждение нового email
    new_token = account_helper.get_activation_token_by_login(login=login)
    assert new_token, 'Не найден токен активации для нового email'
    response = account_api.account_api.put_v1_account_token(token=new_token)
    assert response.status_code == 200, 'Подтверждение нового email не удалось'

    # Авторизация с новым email
    account_helper.user_login(login=login, password=password)
