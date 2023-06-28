from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from auth import deps as auth_deps
from auth.views import auth_router, user_router
from carts.views import cart_router, current_user_cart_router, cart_item_router
from orders.views import order_router
from products.views import product_router as items_router, product_image_router

api_router = APIRouter(
    default_response_class=JSONResponse,
)
authenticated_api_router = APIRouter()

api_router.include_router(auth_router, prefix='/auth', tags=['auth'])
authenticated_api_router.include_router(user_router, prefix='/auth/users', tags=['auth'])

authenticated_api_router.include_router(items_router, prefix='/products', tags=['products'])
authenticated_api_router.include_router(product_image_router, prefix='/products/{product_id}/images', tags=['products'])

authenticated_api_router.include_router(cart_router, prefix='/carts', tags=['carts'])
authenticated_api_router.include_router(current_user_cart_router, prefix='/cart', tags=['carts'])
authenticated_api_router.include_router(cart_item_router, prefix='/cart/items', tags=['carts'])

authenticated_api_router.include_router(order_router, prefix='/orders', tags=['orders'])

api_router.include_router(
    authenticated_api_router,
    dependencies=[
        Depends(auth_deps.get_current_user),
    ],
)
