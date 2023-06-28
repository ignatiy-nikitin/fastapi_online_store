import datetime

from fastapi_mail import MessageSchema, MessageType
from sqlalchemy.orm import Session

import mail_sender
from auth import models as auth_models
from orders import schemas, models


def get_order(db_session: Session, order_id: int) -> models.Order | None:
    return db_session.query(models.Order).filter(models.Order.id == order_id).one_or_none()


def create_order(db_session: Session, user: auth_models.User, order_in: schemas.OrderCreate) -> models.Order:
    order = models.Order(
        **order_in.dict(),
        created_dt=datetime.datetime.now(),
        user=user,
        cart=user.cart,
        status=models.OrderStatus.created,
        total_cost=user.cart.total_cost,
    )
    db_session.add(order)
    db_session.commit()
    return order


def send_email_with_order_info_to_user(order: models.Order):
    mail_message = """Order info.
    
    Created: {created}
    Delivery time: {delivery_dt}
    Address: {address}
    Total cost: {total_cost}
    """.format(
        created=order.created_dt,
        delivery_dt=order.delivery_dt,
        address=order.address,
        total_cost=order.total_cost,
    )

    mail = MessageSchema(
        subject='Fast Api Online Store. Order info.',
        recipients=[order.user.email],
        body=mail_message,
        subtype=MessageType.plain,
    )
    mail_sender.send_mail(mail)
