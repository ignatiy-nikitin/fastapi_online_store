from typing import Annotated

from fastapi import Depends
from jose import JWTError
from sqlalchemy.orm import Session

from auth import models, utils, services, exceptions
from auth.utils import oauth2_scheme
from db import get_db_session


def get_current_user(
        token: str = Depends(oauth2_scheme),
        db_session: Session = Depends(get_db_session),
) -> models.User:
    try:
        payload = utils.decode_jwt_token(token)
    except JWTError:
        raise exceptions.CredentialsException()
    user = services.get_user_by_username(db_session=db_session, username=payload.get('username', ''))
    if user is None:
        raise exceptions.CredentialsException()
    return user


CurrentUser = Annotated[models.User, Depends(get_current_user)]
