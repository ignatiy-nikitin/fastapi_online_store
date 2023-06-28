from fastapi import Depends

from auth import deps as auth_deps
from auth import models as auth_models
from carts import models, deps
from permissions import permission_handler


@permission_handler()
def get_cart_permission(
        current_user: auth_models.User = Depends(auth_deps.get_current_user),
        cart: models.Cart = Depends(deps.valid_cart_id),
):
    return current_user.role == auth_models.UserRoles.admin or cart.user_id == current_user.id


@permission_handler()
def edit_cart_item_permission(
        current_user: auth_models.User = Depends(auth_deps.get_current_user),
        cart_item: models.CartItem = Depends(deps.valid_cart_item_id),
):
    if current_user.role == auth_models.UserRoles.admin:
        return True
    if current_user.cart is not None and cart_item.cart.user.id == current_user.id:
        return True
    return False
