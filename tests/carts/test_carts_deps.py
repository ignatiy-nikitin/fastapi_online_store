import pytest


def test_valid_cart_id(db_session, cart):
    from carts import deps

    t_cart = deps.valid_cart_id(db_session, cart.id)
    assert t_cart
    assert t_cart.id == cart.id


def test_valid_cart_id_error(db_session):
    from carts import deps
    from carts import exceptions

    id_ = 14000

    with pytest.raises(exceptions.CartNotFoundByIdException):
        deps.valid_cart_id(db_session, id_)


def test_valid_cart_item_id(db_session, cart_item):
    from carts import deps

    t_cart_item = deps.valid_cart_item_id(db_session, cart_item.id)
    assert cart_item
    assert t_cart_item.id == cart_item.id


def test_valid_cart_item_id_error(db_session):
    from carts import deps
    from carts import exceptions

    id_ = 14000

    with pytest.raises(exceptions.CartItemNotFoundByIdException):
        deps.valid_cart_item_id(db_session, id_)


def test_valid_product_id_from_cart_item_in(db_session, product):
    from carts import deps
    from carts import schemas

    cart_item_in = schemas.CartItemCreate(
        product_id=product.id,
        quantity=100,
    )

    t_product = deps.valid_product_id_from_cart_item_in(db_session, cart_item_in)
    assert t_product
    assert t_product.id == product.id


def test_valid_product_id_from_cart_item_in_error(db_session, product):
    from carts import deps
    from carts import schemas
    from products import exceptions as products_exceptions

    id_ = 14000

    cart_item_in = schemas.CartItemCreate(
        product_id=id_,
        quantity=100,
    )

    with pytest.raises(products_exceptions.ProductNotFoundByIdException):
        deps.valid_product_id_from_cart_item_in(db_session, cart_item_in)


def test_get_user_cart(db_session, cart):
    from carts import deps

    user = cart.user

    t_cart = deps.get_user_cart(db_session, user)
    assert t_cart
    assert t_cart == user.cart
