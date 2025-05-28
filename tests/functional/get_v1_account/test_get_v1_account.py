def test_get_v1_account_auth(auth_account_helper):
    response = auth_account_helper.dm_account_api.account_api.get_v1_account()
    assert response.status_code == 200, 'Данные о пользователе не были получены'
    user_info = response.json()
    print(user_info)

def test_get_v1_account_no_auth(account_helper):
    account_helper.dm_account_api.account_api.get_v1_account()