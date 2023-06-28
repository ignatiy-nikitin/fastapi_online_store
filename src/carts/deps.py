from fastapi import Depends

from auth import deps as auth_deps
from auth import models as auth_models
from carts import models, services, exceptions, schemas
from db import DbSession
from products import deps as products_deps
from products import models as products_models


def valid_cart_id(
        db_session: DbSession,
        cart_id: int,
) -> models.Cart:
    cart = services.get_cart(db_session, cart_id)
    if cart is None:
        raise exceptions.CartNotFoundByIdException()
    return cart


def valid_cart_item_id(
        db_session: DbSession,
        item_id: int,
) -> models.CartItem:
    cart_item = services.get_cart_item(db_session, item_id)
    if cart_item is None:
        raise exceptions.CartItemNotFoundByIdException()
    return cart_item


def valid_product_id_from_cart_item_in(
        db_session: DbSession,
        cart_item_in: schemas.CartItemCreate,
) -> products_models.Product:
    return products_deps.valid_product_id(db_session, cart_item_in.product_id)


def get_user_cart(
        db_session: DbSession,
        current_user: auth_models.User = Depends(auth_deps.get_current_user),
):
    if current_user.cart is None:
        return services.create_cart(db_session, current_user)
    return current_user.cart
