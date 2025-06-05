from datetime import datetime

from hamcrest import (
    assert_that,
    all_of,
    has_property,
    has_properties,
    equal_to,
    instance_of,
    starts_with,
    has_items,
)


def test_get_v1_account_auth(auth_account_helper):
    response = auth_account_helper.dm_account_api.account_api.get_v1_account(validate_response=True)
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


def test_get_v1_account_no_auth(account_helper):
    account_helper.dm_account_api.account_api.get_v1_account()