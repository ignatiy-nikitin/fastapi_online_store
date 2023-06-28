import os

from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import FileResponse
from fastapi_cache.decorator import cache
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from db import DbSession
from products import schemas, responses, services, models, deps, permissions
from settings import STATIC_FILES_DIR

product_router = APIRouter()
product_image_router = APIRouter()


@product_router.get(
    '',
    response_model=Page[responses.ProductRead],
)
def get_products(
        db_session: DbSession,
):
    return paginate(db_session, services.get_products_query(db_session))


@product_router.get(
    '/{product_id}',
    response_model=responses.ProductRead,
)
@cache(expire=60 * 60)
def get_product(
        product: models.Product = Depends(deps.valid_product_id),
):
    return product


@product_router.post(
    '',
    dependencies=[
        Depends(permissions.edit_product_permission),
    ],
    response_model=responses.ProductRead,
)
def create_product(
        db_session: DbSession,
        product_in: schemas.ProductCreateUpdate,
):
    return services.create_product(db_session, product_in)


@product_router.put(
    '/{product_id}',
    dependencies=[
        Depends(permissions.edit_product_permission),
    ],
    response_model=responses.ProductRead,
)
def update_product(
        db_session: DbSession,
        product_in: schemas.ProductCreateUpdate,
        product: models.Product = Depends(deps.valid_product_id),
):
    return services.update_product(db_session, product, product_in)


@product_image_router.get(
    '/{image_id}',
)
def get_product_image(
        product_image: models.ProductImage = Depends(deps.valid_product_image_id),
):
    return FileResponse(os.path.join(STATIC_FILES_DIR, product_image.path))


@product_image_router.post(
    '',
    dependencies=[
        Depends(permissions.edit_product_permission),
    ],
    response_model=responses.ProductImageRead,
)
def create_product_image(
        db_session: DbSession,
        product_image_file: UploadFile,  # image file
        product: models.Product = Depends(deps.valid_product_id),
):
    path = services.save_product_image_to_static_folder(product_image_file)
    return services.create_product_image(db_session, product, path)
