import datetime


def test_create_order(db_session, cart_item):
    from orders import services
    from orders import schemas
    from orders import models
    
    cart = cart_item.cart
    user = cart.user
    
    delivery_dt = datetime.datetime.now()
    address = 'test address'
    
    order_in = schemas.OrderCreate(
        delivery_dt=delivery_dt,
        address=address,
    )
    order = services.create_order(db_session, user, order_in)
    
    assert order
    assert order.delivery_dt == delivery_dt
    assert order.address == address
    assert order.created_dt
    assert order.user_id == user.id
    assert order.cart_id == cart.id
    assert order.status == models.OrderStatus.created
    assert order.total_cost == cart.total_cost


def test_send_email_with_order_info_to_user(db_session, order):
    import settings
    from orders import services

    order.user.email = settings.MAIL_FROM
    services.send_email_with_order_info_to_user(order)


def test_get_order(db_session, order):
    from orders import services

    assert services.get_order(db_session, order.id)
