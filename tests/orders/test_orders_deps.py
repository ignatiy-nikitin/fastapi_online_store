import pytest


def test_valid_order_id_ok(db_session, order):
    from orders import deps

    assert deps.valid_order_id(db_session, order.id)


def test_valid_order_id_error(db_session):
    from orders import deps, exceptions

    order_id = 14000

    with pytest.raises(exceptions.OrderNotFoundByIdException):
        deps.valid_order_id(db_session, order_id)
