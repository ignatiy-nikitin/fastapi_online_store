from fastapi import Depends

from db import DbSession
from products import services, exceptions, models


def valid_product_id(
        db_session: DbSession,
        product_id: int,
) -> models.Product:
    product = services.get_product(db_session, product_id)
    if product is None:
        raise exceptions.ProductNotFoundByIdException()
    return product


def valid_product_image_id(
        db_session: DbSession,
        image_id: int,
        _: models.Product = Depends(valid_product_id),
) -> models.ProductImage:
    product_image = services.get_product_image(db_session, image_id)
    if product_image is None:
        raise exceptions.ProductImageNotFoundByIdException()
    return product_image
