from datetime import datetime
from dm_api_account.models.user_details_envelope import UserRole
from assertpy import assert_that as assertpy_that, soft_assertions
from hamcrest import (
    assert_that,
    all_of,
    has_property,
    has_properties,
    starts_with,
    has_items,
    instance_of,
    equal_to,
)

from dm_api_account.models.user_details_envelope import UserDetailsEnvelope
from dm_api_account.models.user_envelope import UserRole


class GetV1Account:

    @classmethod
    def check_response_value(
            cls,
            response: UserDetailsEnvelope
    ):
        assert_that(
            response, all_of(
                has_property('resource', has_property('login', starts_with('katya_1'))),
                has_property('resource', has_property('roles', has_items("Guest", "Player"))),
                has_property('resource', has_property('registration', instance_of(datetime))),
                has_property(
                    'resource', has_properties(
                        {
                            'rating': has_properties(
                                {
                                    "enabled": equal_to(True),
                                    "quality": equal_to(0),
                                    "quantity": equal_to(0)
                                }
                            )
                        }
                    )
                )
            )
        )
    @classmethod
    def check_response_soft(
            cls,
            response
    ):
        with soft_assertions():
            assertpy_that(response.resource.login).starts_with('katya_1')
            assertpy_that(response.resource.online).is_instance_of(datetime)
            assertpy_that(response.resource.roles).contains(UserRole.GUEST, UserRole.PLAYER)