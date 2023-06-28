from fastapi import APIRouter, Depends, BackgroundTasks

from auth import deps as auth_deps
from db import DbSession
from orders import schemas, responses, services, models, deps, permissions

order_router = APIRouter()


@order_router.get(
    '/{order_id}',
    response_model=responses.OrderRead,
    dependencies=[
        Depends(permissions.get_order_permission),
    ]
)
def get_order(
        order: models.Order = Depends(deps.valid_order_id),
):
    return order


@order_router.post(
    '',
    response_model=responses.OrderRead,
)
def create_order(
        db_session: DbSession,
        background_tasks: BackgroundTasks,
        order_in: schemas.OrderCreate,
        current_user=Depends(auth_deps.get_current_user),
):
    order = services.create_order(db_session, current_user, order_in)
    background_tasks.add_task(
        services.send_email_with_order_info_to_user, order,
    )
    return order
