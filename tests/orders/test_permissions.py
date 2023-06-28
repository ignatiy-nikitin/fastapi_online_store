import pytest


def test_get_order_permission__admin_access_ok(user_admin, order):
    from orders import permissions

    assert permissions.get_order_permission(user_admin, order)


def test_get_order_permission__operator_access_ok(user_operator, order):
    from orders import permissions

    assert permissions.get_order_permission(user_operator, order)


def test_get_order_permission__user_access_his_order_ok(order):
    from orders import permissions

    user = order.user
    assert permissions.get_order_permission(user, order)


def test_get_order_permission__user_access_not_his_order_error(user_client, order):
    from orders import permissions
    import exceptions

    with pytest.raises(exceptions.PermissionDeniedException):
        permissions.get_order_permission(user_client, order)
