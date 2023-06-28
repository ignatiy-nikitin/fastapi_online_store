import pytest

from exceptions import PermissionDeniedException


def test_edit_product_by_client(user_client):
    from products import permissions

    with pytest.raises(PermissionDeniedException):
        permissions.edit_product_permission(user_client)


def test_edit_product_by_operator(user_operator):
    from products import permissions

    assert permissions.edit_product_permission(user_operator)


def test_edit_product_by_admin(user_admin):
    from products import permissions

    assert permissions.edit_product_permission(user_admin)
