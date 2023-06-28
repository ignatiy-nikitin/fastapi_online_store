from sqlalchemy.orm import Session

from auth import models as auth_models
from carts import models, schemas
from products import models as products_models


def get_cart(db_session: Session, cart_id: int) -> models.Cart | None:
    return db_session.query(models.Cart).filter(models.Cart.id == cart_id).one_or_none()


def create_cart(db_session: Session, user: auth_models.User) -> models.Cart:
    cart = models.Cart(user_id=user.id)
    db_session.add(cart)
    db_session.commit()
    return cart


def get_cart_item(db_session: Session, cart_item_id: int) -> models.CartItem | None:
    return db_session.query(models.CartItem).filter(models.CartItem.id == cart_item_id).one_or_none()


def create_cart_item(db_session: Session, cart: models.Cart, product: products_models.Product,
                     cart_item_in: schemas.CartItemCreate) -> models.CartItem:
    cart_item = models.CartItem(
        **cart_item_in.dict(),
        cart=cart,
        price=product.price,
    )
    db_session.add(cart_item)
    db_session.commit()
    return cart_item


def update_cart_item(db_session: Session, cart_item: models.CartItem,
                     cart_item_in: schemas.CartItemUpdate) -> models.CartItem:
    update_data = cart_item_in.dict()

    for field, update_value in update_data.items():
        setattr(cart_item, field, update_value)

    db_session.commit()
    db_session.refresh(cart_item)
    return cart_item


def delete_cart_item(db_session: Session, cart_item_id: int):
    db_session.query(models.CartItem).filter(models.CartItem.id == cart_item_id).delete()
    db_session.commit()
