import os.path

from fastapi import UploadFile


def test_get_products_query(db_session, product):
    from products import services

    t_products = services.get_products_query(db_session)
    assert t_products
    assert t_products.all()


def test_get_product(db_session, product):
    from products import services

    t_product = services.get_product(db_session, product.id)
    assert t_product


def test_create_product(db_session):
    from decimal import Decimal
    from products import schemas
    from products import services

    title = 'test title'
    description = 'test description'
    price = Decimal(100.00)

    product_in = schemas.ProductCreateUpdate(
        title=title,
        description=description,
        price=price,
    )
    product = services.create_product(db_session, product_in)

    assert product
    assert product.title == title
    assert product.description == description
    assert product.price == price


def test_save_product_image_to_static_folder(product, product_image_file):
    from products import services
    from settings import STATIC_FILES_DIR

    image_file = UploadFile(product_image_file)
    image_file.filename = product_image_file.name
    path = services.save_product_image_to_static_folder(image_file)
    assert path
    assert path.endswith('.png')
    assert os.path.isfile(os.path.join(STATIC_FILES_DIR, path))


def test_create_product_image(db_session, product):
    from products import services

    path = 'image.png'

    product_image = services.create_product_image(db_session, product, path)

    assert product_image
    assert product_image.path == path
    assert product_image.product_id == product.id
