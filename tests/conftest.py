
from collections import namedtuple
from datetime import datetime
import random
import string
import pytest
from restclient.configuration import Configuration as MailHogConfiguration
import structlog

from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as DmApiConfiguration
from services.api_mailhog import MailHogApi
from services.dm_api_account import DMApiAccount

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=False, #чтобы были русские буквы
            # sort_keys=True
        )
    ]
)


@pytest.fixture(scope='session')
def mailhog_api():
    mailhog_configuration = MailHogConfiguration(host='http://5.63.153.31:5025')
    mailhog_client = MailHogApi(configuration=mailhog_configuration)
    return mailhog_client


@pytest.fixture(scope='session')
def account_api():
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    account = DMApiAccount(configuration=dm_api_configuration)
    return account


@pytest.fixture(scope='session')
def account_helper(
        account_api,
        mailhog_api
):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog_api)
    return account_helper

@pytest.fixture(scope='session')
def auth_account_helper(mailhog_api):
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    account = DMApiAccount(configuration=dm_api_configuration)
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog_api)
    account_helper.auth_client(
        login='katya_1_caef2a',
        password='Qwerty123!'
    )
    return account_helper

@pytest.fixture
def prepare_user():
    now = datetime.now()
    milliseconds = now.strftime('%f')[:3]  # первые 3 цифры — миллисекунды
    timestamp = now.strftime(f'%d_%m_%Y_%H_%M_%S_{milliseconds}')
    login = f'Katya{timestamp}'
    password = '123456789'
    email = f'{login}@mail.ru'
    User = namedtuple('User', ['login', 'password', 'email'])
    user = User(login=login, password=password, email=email)
    return user


