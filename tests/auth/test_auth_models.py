def test_user_model_check_password_method_ok(user_client):
    password = 'password'
    assert user_client.check_password(password)


def test_user_model_check_password_method_error(user_client):
    password = 'XXX'
    assert not user_client.check_password(password)
