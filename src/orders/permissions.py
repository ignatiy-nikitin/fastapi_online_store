from fastapi import Depends

from auth import deps as auth_deps
from auth import models as auth_models
from orders import models, deps
from permissions import permission_handler


@permission_handler()
def get_order_permission(
        current_user: auth_models.User = Depends(auth_deps.get_current_user),
        order: models.Order = Depends(deps.valid_order_id),
):
    if current_user.role in (auth_models.UserRoles.admin, auth_models.UserRoles.operator):
        return True
    if order.user.id == current_user.id:
        return True
    return False
