def test_create_cart(db_session, user):
    from carts import services
    
    t_cart = services.create_cart(db_session, user)
    assert t_cart
    assert t_cart.user_id == user.id
    
    
def test_update_cart_item(db_session, cart_item):
    from carts import services
    from carts import schemas
    
    quantity = 8742
    
    cart_item_in = schemas.CartItemUpdate(
        quantity=quantity,
    )
    
    t_cart_item = services.update_cart_item(db_session, cart_item, cart_item_in)
    assert t_cart_item
    assert t_cart_item.quantity == quantity


def test_delete_cart_item(db_session, cart_item):
    from carts import services
    
    services.delete_cart_item(db_session, cart_item.id)
    assert not services.get_cart_item(db_session, cart_item.id)
