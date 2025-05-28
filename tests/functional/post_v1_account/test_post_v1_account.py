from data import generate_user
import structlog
from restclient.configuration import Configuration as DmApiConfiguration
from services.dm_api_account import DMApiAccount

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            #ensure_ascii=True,
            #sort_keys=True
        )
    ]
)

def test_post_v1_account():
    # Инициализация клиентов
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)

    account = DMApiAccount(configuration=dm_api_configuration)

    login, email, password = generate_user()

    # Регистрация пользователя
    response = account.account_api.post_v1_account(json_data={
        'login': login,
        'email': email,
        'password': password,
    })
    assert response.status_code == 201, f'Пользователь не был создан: {response.text}'

