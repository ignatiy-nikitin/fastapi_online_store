from fastapi import APIRouter, Depends

from carts import models, permissions, responses, schemas, services, deps
from db import DbSession
from products import models as products_models

cart_router = APIRouter()
current_user_cart_router = APIRouter()
cart_item_router = APIRouter()


@cart_router.get(
    '/{cart_id}',
    dependencies=[
        Depends(permissions.get_cart_permission),
    ],
    response_model=responses.CartRead,
)
def get_cart(
        cart: models.Cart = Depends(deps.valid_cart_id),
):
    return cart


@current_user_cart_router.get(
    '',
    response_model=responses.CartRead,
)
def get_current_user_cart(
        user_cart: models.Cart = Depends(deps.get_user_cart),
):
    return user_cart


@cart_item_router.post(
    '',
    response_model=responses.CartItemRead,
)
def create_cart_item(
        db_session: DbSession,
        cart_item_in: schemas.CartItemCreate,
        user_cart: models.Cart = Depends(deps.get_user_cart),
        product: products_models.Product = Depends(deps.valid_product_id_from_cart_item_in),
):
    return services.create_cart_item(db_session, user_cart, product, cart_item_in)


@cart_item_router.put(
    '/{item_id}',
    dependencies=[
        Depends(permissions.edit_cart_item_permission),
    ],
    response_model=responses.CartItemRead,
)
def update_cart_item(
        db_session: DbSession,
        cart_item_in: schemas.CartItemUpdate,
        cart_item: models.CartItem = Depends(deps.valid_cart_item_id),
):
    return services.update_cart_item(db_session, cart_item, cart_item_in)


@cart_item_router.delete(
    '/{item_id}',
    dependencies=[
        Depends(permissions.edit_cart_item_permission),
    ],
)
def delete_cart_item(
        db_session: DbSession,
        cart_item: models.CartItem = Depends(deps.valid_cart_item_id),
):
    services.delete_cart_item(db_session, cart_item.id)
