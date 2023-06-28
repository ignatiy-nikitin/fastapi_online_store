import pytest


def test_valid_product_id(db_session, product):
    from products import deps

    t_product = deps.valid_product_id(db_session, product.id)
    assert t_product
    assert t_product.id == product.id


def test_valid_product_id_error(db_session):
    from products import deps
    from products import exceptions

    id_ = 14000

    with pytest.raises(exceptions.ProductNotFoundByIdException):
        deps.valid_product_id(db_session, id_)


def test_valid_product_image_id(db_session, product_image):
    from products import deps

    t_product_image = deps.valid_product_image_id(db_session, product_image.id)
    assert t_product_image
    assert t_product_image.id == product_image.id


def test_valid_product_image_id_error(db_session):
    from products import deps
    from products import exceptions

    id_ = 14000

    with pytest.raises(exceptions.ProductImageNotFoundByIdException):
        deps.valid_product_image_id(db_session, id_)
