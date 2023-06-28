from fastapi import status


# def test_get_order_view(client, order):
#     response = client.get(
#         url=f'orders/{order.id}',
#         headers={
#             'Authorization': f'Bearer {user.jwt_token}',
#         }
#     )


def test_create_order_view(client, cart):
    user = cart.user
    data = {
        'delivery_dt': '2023-05-30T10:32:47.352Z',
        'address': 'XXX',
    }
    response = client.post(
        url='orders',
        json=data,
        headers={
            'Authorization': f'Bearer {user.jwt_token}',
        }
    )
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert response.json()
    assert 'id' in response.json()
    assert 'created_dt' in response.json()
    assert 'address' in response.json()
    assert response.json()['address'] == data['address']
    assert 'status' in response.json()
    assert 'total_cost' in response.json()
