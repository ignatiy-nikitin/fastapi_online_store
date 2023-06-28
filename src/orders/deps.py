from db import DbSession
from orders import models, services, exceptions


def valid_order_id(
        db_session: DbSession,
        order_id: int,
) -> models.Order:
    order = services.get_order(db_session, order_id)
    if order is None:
        raise exceptions.OrderNotFoundByIdException()
    return order
