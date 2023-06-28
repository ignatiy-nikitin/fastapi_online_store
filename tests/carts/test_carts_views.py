from fastapi import status


def test_get_cart__admin_can_get_any_cart(client, user_admin, cart):
    response = client.get(
        url=f'carts/{cart.id}',
        headers={
            'Authorization': f'Bearer {user_admin.jwt_token}',
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()
    assert 'id' in response.json()
    assert response.json()['id'] == cart.id


def test_get_cart_operator_can_not_get_any_cart(client, user_operator, cart):
    response = client.get(
        url=f'carts/{cart.id}',
        headers={
            'Authorization': f'Bearer {user_operator.jwt_token}',
        }
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_cart__client_can_not_get_not_his_cart(client, user_client, cart):
    response = client.get(
        url=f'carts/{cart.id}',
        headers={
            'Authorization': f'Bearer {user_client.jwt_token}',
        }
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_current_user_cart(client, user_client):
    response = client.get(
        url=f'cart',
        headers={
            'Authorization': f'Bearer {user_client.jwt_token}',
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()
    assert 'id' in response.json()
    assert response.json()['id'] == user_client.cart.id


def test_create_cart_item(client, user_client, product):
    data_to_save = {
        'product_id': product.id,
        'quantity': 10,
    }
    response = client.post(
        url='cart/items',
        json=data_to_save,
        headers={
            'Authorization': f'Bearer {user_client.jwt_token}',
        }
    )
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()
    assert 'id' in response.json()
    assert 'quantity' in response.json()
    assert response.json()['quantity'] == data_to_save['quantity']


def test_delete_cart_item__user_can_delete_his_cart_item(client, cart_item):
    user = cart_item.cart.user
    response = client.delete(
        url=f'cart/items/{cart_item.id}',
        headers={
            'Authorization': f'Bearer {user.jwt_token}',
        }
    )
    assert response.status_code == status.HTTP_200_OK, response.json()
    
    
def test_delete_cart_item__client_cant_delete_not_his_cart_item(client, user_client, cart_item):
    response = client.delete(
        url=f'cart/items/{cart_item.id}',
        headers={
            'Authorization': f'Bearer {user_client.jwt_token}',
        }
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    
    
def test_delete_cart_item___operator_cant_delete_not_his_cart_item(client, user_operator, cart_item):
    response = client.delete(
        url=f'cart/items/{cart_item.id}',
        headers={
            'Authorization': f'Bearer {user_operator.jwt_token}',
        }
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    
    
def test_delete_cart_item___admin_can_delete_any_cart_item(client, user_admin, cart_item):
    response = client.delete(
        url=f'cart/items/{cart_item.id}',
        headers={
            'Authorization': f'Bearer {user_admin.jwt_token}',
        }
    )
    assert response.status_code == status.HTTP_200_OK
