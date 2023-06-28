from sqlalchemy.orm import Session

from auth import models, schemas


def get_user_by_username(db_session: Session, username: str) -> models.User | None:
    return db_session.query(models.User).filter(models.User.username == username).one_or_none()


def create_user(db_session: Session, user_register: schemas.UserRegister) -> models.User:
    user = models.User(**user_register.dict())
    db_session.add(user)
    db_session.commit()
    return user


def update_user(db_session: Session, user: models.User, user_in: schemas.UserUpdateBase) -> models.User:
    update_data = user_in.dict()
    for field, update_value in update_data.items():
        setattr(user, field, update_value)
    db_session.commit()
    db_session.refresh(user)
    return user
