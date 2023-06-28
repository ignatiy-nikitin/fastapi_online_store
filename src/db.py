from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker, Session

from settings import DB_URI

engine = create_engine(DB_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)


def get_db_session():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


DbSession = Annotated[Session, Depends(get_db_session)]


class BaseDBModel(DeclarativeBase):
    from_orm = True


def create_all_db_tables():
    from auth import models  # noqa
    from carts import models  # noqa
    from orders import models  # noqa
    from products import models  # noqa
    BaseDBModel.metadata.create_all(bind=engine)
