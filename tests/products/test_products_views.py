import time

from fastapi import status


def test_get_products_ok(client, user_client, product):
    response = client.get(
        url='products',
        headers={
            'Authorization': f'Bearer {user_client.jwt_token}',
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()
    assert 'total' in response.json()
    assert 'page' in response.json()
    assert 'size' in response.json()
    assert 'pages' in response.json()
    assert 'items' in response.json()
    assert response.json()['items']
    response_product = response.json()['items'][0]
    assert 'id' in response_product
    assert 'title' in response_product
    assert 'description' in response_product
    assert 'price' in response_product
    assert 'images' in response_product
    response_image = response_product['images'][0]
    assert 'id' in response_image
    assert 'path' in response_image


def test_get_product_ok(client, user_client, product):
    response = client.get(
        url=f'products/{product.id}',
        headers={
            'Authorization': f'Bearer {user_client.jwt_token}',
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()
    assert 'id' in response.json()
    assert response.json()['id'] == product.id
    assert 'title' in response.json()
    assert response.json()['title'] == product.title
    assert 'description' in response.json()
    assert response.json()['description'] == product.description
    assert 'price' in response.json()
    assert response.json()['price'] == float(product.price)
    assert 'images' in response.json()
    assert response.json()['images']
    response_image = response.json()['images'][0]
    assert response_image
    assert 'id' in response_image
    assert 'path' in response_image


def test_get_product_cache_ok(client, user_operator, product):
    response = client.get(
        url=f'products/{product.id}',
        headers={
            'Authorization': f'Bearer {user_operator.jwt_token}',
        }
    )
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()
    # time.sleep(4)

    product_data_to_update = {
        'title': response.json()['title'],
        'description': response.json()['description'],
        'price': 184665,
    }
    response = client.put(
        f'products/{product.id}',
        json=product_data_to_update,
        headers={
            'Authorization': f'Bearer {user_operator.jwt_token}',
        }
    )
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()
    assert response.json()['price'] == product_data_to_update['price']

    response = client.get(
        url=f'products/{product.id}',
        headers={
            'Authorization': f'Bearer {user_operator.jwt_token}',
        }
    )
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()
    assert response.json()['price'] == product_data_to_update['price']


def test_update_product_user_client_permission_error(client, user_client, product):
    data_to_update = {
        'title': 'XXX',
        'description': 'XXX',
        'price': 184665,
    }

    response = client.put(
        f'products/{product.id}',
        json=data_to_update,
        headers={
            'Authorization': f'Bearer {user_client.jwt_token}',
        }
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_product_user_operator_permission_ok(client, user_operator, product):
    data_to_update = {
        'title': 'XXX',
        'description': 'XXX',
        'price': 184665,
    }

    response = client.put(
        f'products/{product.id}',
        json=data_to_update,
        headers={
            'Authorization': f'Bearer {user_operator.jwt_token}',
        }
    )

    assert response.status_code == status.HTTP_200_OK


def test_update_product_user_admin_ok(client, user_admin, product):
    data_to_update = {
        'title': 'XXX',
        'description': 'XXX',
        'price': 184665,
    }

    response = client.put(
        f'products/{product.id}',
        json=data_to_update,
        headers={
            'Authorization': f'Bearer {user_admin.jwt_token}',
        }
    )

    assert response.status_code == status.HTTP_200_OK


def test_update_product_ok(client, user_admin, product, db_session):
    data_to_update = {
        'title': 'XXX',
        'description': 'XXX',
        'price': 184665,
    }

    response = client.put(
        f'products/{product.id}',
        json=data_to_update,
        headers={
            'Authorization': f'Bearer {user_admin.jwt_token}',
        }
    )

    assert response.status_code == status.HTTP_200_OK

    # product = services.get_product(db_session, product.id)
    assert response.json()
    assert 'title' in response.json()
    assert response.json()['title'] == data_to_update['title']
    assert 'description' in response.json()
    assert response.json()['description'] == data_to_update['description']
    assert 'price' in response.json()
    assert response.json()['price'] == data_to_update['price']


def test_create_product_image_user_client_permission_error(client, user_client, product):
    data_to_create = {
        'path': 'test.png',
        'order': 1,
    }
    response = client.post(
        url=f'products/{product.id}/images',
        json=data_to_create,
        headers={
            'Authorization': f'Bearer {user_client.jwt_token}',
        }
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_product_image_user_operator_permission_ok(client, user_operator, product, product_image_file):
    response = client.post(
        url=f'products/{product.id}/images',
        files={'product_image_file': product_image_file},
        headers={
            'Authorization': f'Bearer {user_operator.jwt_token}',
        }
    )
    assert response.status_code == status.HTTP_200_OK, response.json()


def test_create_product_image_user_admin_permission_ok(client, user_admin, product, product_image_file):
    response = client.post(
        url=f'products/{product.id}/images',
        files={'product_image_file': product_image_file},
        headers={
            'Authorization': f'Bearer {user_admin.jwt_token}',
        }
    )
    assert response.status_code == status.HTTP_200_OK


def test_create_product_image_ok(client, user_admin, product, product_image_file):
    response = client.post(
        url=f'products/{product.id}/images',
        files={'product_image_file': product_image_file},
        headers={
            'Authorization': f'Bearer {user_admin.jwt_token}',
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()
    assert 'path' in response.json()


def test_create_product_image_ok2(client, user_admin, product, product_image_file):
    response = client.post(
        url=f'products/{product.id}/images',
        files={'product_image_file': product_image_file},
        headers={
            'Authorization': f'Bearer {user_admin.jwt_token}',
        },
    )
    assert response.status_code == status.HTTP_200_OK


def test_get_product_image(client, user_client, product_image):
    response = client.get(
        url=f'products/{product_image.product.id}/images/{product_image.id}',
        headers={
            'Authorization': f'Bearer {user_client.jwt_token}',
        },
    )
    assert response.status_code == status.HTTP_200_OK
