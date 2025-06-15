import os
import shutil
from collections import namedtuple
from datetime import datetime
import random
import string
from pathlib import Path

from requests.auth import HTTPBasicAuth
from swagger_coverage_py.reporter import CoverageReporter
from vyper import v
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
            ensure_ascii=False
            # sort_keys=True
        )
    ]
)

options = (
    'service.dm_api_account',
    'service.mailhog',
    'user.login',
    'user.password'
)

@pytest.fixture(scope="session", autouse=True)
def setup_swagger_coverage():
    reporter = CoverageReporter(api_name="dm-api-account", host="http://5.63.153.31:5051")
    reporter.cleanup_input_files()
    reporter.setup("/swagger/Account/swagger.json")

    yield
    reporter.generate_report()
    print(f"Current working dir: {os.getcwd()}")
    report_path = Path("swagger-coverage-dm-api-account.html")
    print(f"Report exists: {report_path.exists()} at {report_path.absolute()}")



@pytest.fixture(scope='function', autouse=True)
def set_config(request):
    config = Path(__file__).joinpath('../../').joinpath('config')
    config_name = request.config.getoption('--env')
    v.set_config_name(config_name)
    v.add_config_path(config)
    v.read_in_config()
    for option in options:
        v.set(f'{option}', request.config.getoption(f'--{option}'))


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

    now = datetime.now()
    data = now.strftime('%d_%m_%Y_%H_%M_%S_%f')[:-3]
    login = f'Katya{data}'
    password = '123456789'
    email = f'{login}@mail.ru'
    User = namedtuple('User', ['login', 'password', 'email'])
    user = User(login=login, password=password, email=email)
    return user

