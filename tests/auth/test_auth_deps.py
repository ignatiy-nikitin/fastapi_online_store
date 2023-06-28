import pytest


def test_get_current_user_ok(db_session, user):
    from auth import deps

    t_user = deps.get_current_user(user.jwt_token, db_session)
    assert t_user
    assert t_user.id == user.id


def test_get_current_user_error(db_session):
    from auth import deps
    from auth import exceptions

    token = 'Bearer invalid_test_jwt_token'
    with pytest.raises(exceptions.CredentialsException):
        deps.get_current_user(token, db_session)
