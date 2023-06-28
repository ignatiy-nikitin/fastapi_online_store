from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth import schemas, services, deps, responses, exceptions
from db import get_db_session, DbSession

auth_router = APIRouter()
user_router = APIRouter()


@auth_router.post(
    '/register',
    response_model=responses.UserRead,
)
def register_user_view(
        user_register: schemas.UserRegister,
        db_session: Session = Depends(get_db_session),
):
    user = services.get_user_by_username(db_session, user_register.username)
    if user:
        raise exceptions.UserWithThisUsernameAlreadyExistsException()
    return services.create_user(db_session, user_register)


@auth_router.post(
    '/login',
    response_model=responses.Token,
)
def login_view(
        user_login=Depends(OAuth2PasswordRequestForm),
        db_session: Session = Depends(get_db_session),
):
    user = services.get_user_by_username(db_session, user_login.username)
    if user and user.check_password(user_login.password):
        return responses.Token(access_token=user.jwt_token)
    raise exceptions.InvalidLoginDataException()


@user_router.get(
    '/me',
    response_model=responses.UserRead,
)
def user_me_view(
        current_user: deps.CurrentUser,
):
    return current_user


@user_router.put(
    '/me',
    response_model=responses.UserRead,
)
def user_me_update(
        db_session: DbSession,
        current_user: deps.CurrentUser,
        user_in: schemas.UserUpdateBase,
):
    return services.update_user(db_session, current_user, user_in)
