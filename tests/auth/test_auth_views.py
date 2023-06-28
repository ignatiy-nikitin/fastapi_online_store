from fastapi import status


def test_register_user_ok(client):
    data_to_create = {
        'email': '123@gmail.com',
        'username': 'username_test_register_user',
        'password': 'password',
        'name': 'name',
        'age': 20,
    }
    response = client.post(
        url='auth/register',
        json=data_to_create,
    )
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()
    assert 'email' in response.json()
    assert response.json()['email'] == data_to_create['email']
    assert 'name' in response.json()
    assert response.json()['name'] == data_to_create['name']
    assert 'age' in response.json()
    assert response.json()['age'] == data_to_create['age']
    assert 'password' not in response.json()


def test_register_user__user_with_username_already_exists_error(client, user):
    data_to_create = {
        'email': user.email,
        'username': user.username,
        'password': 'password',
        'name': 'name',
        'age': 20,
    }
    response = client.post(
        url='auth/register',
        json=data_to_create,
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN, response.json()
    assert response.json() == {'detail': 'User with username already exists.'}


def test_login_view_ok(client, user):
    data = {
        'username': user.username,
        'password': 'password',
    }
    response = client.post(
        url='auth/login',
        data=data,
    )
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()
    assert 'access_token' in response.json()
    assert response.json()['access_token']
    assert 'token_type' in response.json()
    assert response.json()['token_type'] == 'bearer'


def test_login_view__invalid_login_data_error(client, user):
    data = {
        'username': 'XXX',
        'password': 'XXX',
    }
    response = client.post(
        url='auth/login',
        data=data,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.json()
    assert response.json() == {'detail': 'Invalid login data.'}


def test_get_user_me_view_ok(client, user):
    response = client.get(
        url='auth/users/me',
        headers={
            'Authorization': f'Bearer {user.jwt_token}',
        }
    )
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()
    assert 'email' in response.json()
    assert response.json()['email'] == user.email
    assert 'name' in response.json()
    assert response.json()['name'] == user.name
    assert 'age' in response.json()
    assert response.json()['age'] == user.age
    assert 'role' in response.json()
    assert response.json()['role'] == user.role.value
    assert 'password' not in response.json()


def test_user_me_update(client, user):
    data = {
        'password': 'newpassword',
        'name': 'new name',
        'age': 50,
    }
    response = client.put(
        url='auth/users/me',
        json=data,
        headers={
            'Authorization': f'Bearer {user.jwt_token}',
        }
    )
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()
    assert 'name' in response.json()
    assert response.json()['name'] == data['name']
    assert 'age' in response.json()
    assert response.json()['age'] == data['age']
