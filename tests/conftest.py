import os
from collections import namedtuple
from datetime import datetime
from pathlib import Path
import swagger_coverage_py
from swagger_coverage_py.reporter import CoverageReporter
from vyper import v
import pytest
import sys
from packages.notifier.bot import send_file
from packages.restclient.configuration import Configuration as MailHogConfiguration
import structlog

from helpers.account_helper import AccountHelper
from packages.restclient.configuration import Configuration as DmApiConfiguration
from services.api_mailhog import MailHogApi
from services.dm_api_account import DMApiAccount

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=False
            # sort_keys=True
        )
    ]
)

options = (
    'service.dm_api_account',
    'service.mailhog',
    'user.login',
    'user.password',
    'telegram.chat_id',
    'telegram.token'
)

@pytest.fixture(scope="session", autouse=True)
def setup_swagger_coverage():
    reporter = CoverageReporter(api_name="dm-api-account", host="http://5.63.153.31:5051")
    reporter.setup("/swagger/Account/swagger.json")

    yield
    reporter.generate_report()
    reporter.cleanup_input_files()
    send_file()

@pytest.fixture(scope='function', autouse=True)
def set_config(request):
    config = Path(__file__).joinpath('../../').joinpath('config')
    config_name = request.config.getoption('--env')
    v.set_config_name(config_name)
    v.add_config_path(config)
    v.read_in_config()
    for option in options:
        v.set(f'{option}', request.config.getoption(f'--{option}'))
    os.environ['TELEGRAM_BOT_CHAT_ID'] = v.get('telegram.chat_id')
    os.environ['TELEGRAM_BOT_ACCESS_TOKEN'] = v.get('telegram.token')
    request.config.stash['telegram-notifier-addfields']['environment'] = config_name
    request.config.stash['telegram-notifier-addfields']['report'] = 'https://ekaterinavolynkina.github.io/dm_api_tests/'





def pytest_addoption(
        parser
        ):
    parser.addoption('--env', action='store', default='stg', help='run stg')

    for option in options:
        parser.addoption(f'--{option}', action='store', default=None)


@pytest.fixture(scope='function')
def mailhog_api():
    mailhog_configuration = MailHogConfiguration(host=v.get('service.mailhog'), disable_log=False)
    mailhog_client = MailHogApi(configuration=mailhog_configuration)
    return mailhog_client


@pytest.fixture(scope='function')
def account_api():
    dm_api_configuration = DmApiConfiguration(host=v.get('service.dm_api_account'), disable_log=False)
    account = DMApiAccount(configuration=dm_api_configuration)
    return account


@pytest.fixture(scope='function')
def account_helper(
        account_api,
        mailhog_api
):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog_api)
    return account_helper

@pytest.fixture(scope='function')
def auth_account_helper(mailhog_api):
    dm_api_configuration = DmApiConfiguration(host=v.get('service.dm_api_account'), disable_log=False)
    account = DMApiAccount(configuration=dm_api_configuration)
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog_api)
    account_helper.auth_client(
        login=v.get('user.login'),
        password=v.get('user.password')
    )
    return account_helper

@pytest.fixture
def prepare_user():
    now = datetime.now().strftime('%d%m%Y_%H%M%S%f')[:-3]
    login = f'Katya_{now}'[:30]
    password = v.get('user.password')
    email = f'{login}@mail.ru'
    User = namedtuple('User', ['login', 'password', 'email'])
    user = User(login=login, password=password, email=email)
    return user
