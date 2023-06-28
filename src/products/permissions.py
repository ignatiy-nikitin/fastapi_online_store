from fastapi import Depends

from auth import deps as auth_deps
from auth import models as auth_models
from permissions import permission_handler


@permission_handler()
def edit_product_permission(
        current_user: auth_models.User = Depends(auth_deps.get_current_user),
):
    return current_user.role in (auth_models.UserRoles.operator, auth_models.UserRoles.admin)
