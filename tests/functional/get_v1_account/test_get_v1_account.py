from datetime import datetime
from assertpy import assert_that as assertpy_that, soft_assertions

from hamcrest import (
    assert_that as hamcrest_that,
    all_of,
    has_property,
    starts_with,
    has_items,
    instance_of,
    has_properties,
    equal_to,
)

from checkers.http_checkers import check_status_code_http
from dm_api_account.models.user_details_envelope import UserRole


def test_get_v1_account_auth(auth_account_helper):
    response = auth_account_helper.dm_account_api.account_api.get_v1_account(validate_response=True)
    with soft_assertions():
        assertpy_that(response.resource.login).starts_with('katya_1')
        assertpy_that(response.resource.online).is_instance_of(datetime)
        assertpy_that(response.resource.roles).contains(UserRole.GUEST, UserRole.PLAYER)






    # проверки hamcrest
    # hamcrest_that(
    #     response, all_of(
    #         has_property('resource', has_property('login', starts_with('katya_1'))),
    #         has_property('resource', has_property('roles', has_items("Guest", "Player"))),
    #         has_property('resource', has_property('registration', instance_of(datetime))),
    #         has_property(
    #             'resource', has_properties(
    #                 {
    #                     'rating': has_properties(
    #                         {
    #                             "enabled": equal_to(True),
    #                             "quality": equal_to(0),
    #                             "quantity": equal_to(0)
    #                         }
    #                     )
    #                 }
    #             )
    #         )
    #     )
    # )
    # print(response)
def test_get_v1_account_no_auth(account_helper):
    with check_status_code_http(401, 'User must be authenticated'):
        account_helper.dm_account_api.account_api.get_v1_account()