from pydantic import EmailStr


def test_get_user_by_username(db_session, user):
    from auth import services

    t_user = services.get_user_by_username(db_session, user.username)
    assert t_user


def test_create_user(db_session):
    from auth import services, schemas, models, utils

    email = EmailStr('test@test.com')
    username = 'username'
    password = 'password'
    name = 'test name'
    age = 19
    role = models.UserRoles.client

    user_in = schemas.UserRegister(
        email=email,
        username=username,
        password=password,
        name=name,
        age=age,
        role=role,
    )
    user = services.create_user(db_session, user_in)

    assert user
    assert user.email == email
    assert user.name == name
    assert user.age == age
    assert user.role == role

    assert utils.verify_password(password, user.password)


def test_update_user(db_session, user):
    from auth import services
    from auth import models
    from auth import schemas

    password = 'password'
    name = 'XXX'
    age = 40
    role = models.UserRoles.operator

    user_in = schemas.UserUpdate(
        name=name,
        age=age,
        password=password,
        role=role,
    )
    t_user = services.update_user(db_session, user, user_in)
    assert t_user
