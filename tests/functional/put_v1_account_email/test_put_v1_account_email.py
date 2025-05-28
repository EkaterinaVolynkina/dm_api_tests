import uuid
from data import generate_user
from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as DmApiConfiguration
from restclient.configuration import Configuration as MailHogConfiguration
import structlog
from services.api_mailhog import MailHogApi
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

def test_post_v1_account_email():
    # Инициализация клиентов
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    mailhog_configuration = MailHogConfiguration(host='http://5.63.153.31:5025')

    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)


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
    # Подтверждение нового email

    account_helper.change_mail(login=login, password=password, new_email=new_email)

    # Авторизация с новым email
    account_helper.user_login(login=login, password=password)
