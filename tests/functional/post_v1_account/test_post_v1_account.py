from data import generate_user
import structlog
from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as DmApiConfiguration
from restclient.configuration import Configuration as MailHogConfiguration
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi

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
    mailhog_configuration = MailHogConfiguration(host='http://5.63.153.31:5025')

    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

    login, email, password = generate_user()
    account_helper.register_new_user(login=login, password=password, email=email)

