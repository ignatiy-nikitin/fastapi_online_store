import os
import shutil
import uuid
from pathlib import Path

from sqlalchemy.orm import Session

from products import schemas, models
from settings import STATIC_FILES_DIR


def create_product(db_session: Session, product_in: schemas.ProductCreateUpdate) -> models.Product:
    product = models.Product(**product_in.dict(exclude={'product_images'}))
    db_session.add(product)
    db_session.commit()
    return product


def update_product(db_session: Session, product: models.Product,
                   product_in: schemas.ProductCreateUpdate) -> models.Product:
    update_data = product_in.dict()

    for field, update_value in update_data.items():
        setattr(product, field, update_value)

    db_session.commit()
    db_session.refresh(product)
    return product


def get_products_query(db_session: Session):
    return db_session.query(models.Product)


def get_product(db_session: Session, product_id: int) -> models.Product | None:
    return db_session.query(models.Product).filter(models.Product.id == product_id).one_or_none()


def get_product_image(db_session: Session, product_image_id: int) -> models.ProductImage | None:
    return db_session.query(models.ProductImage).filter(models.ProductImage.id == product_image_id).one_or_none()


def save_product_image_to_static_folder(product_image_file) -> str:
    file_ext = product_image_file.filename.split('.')[1]
    unique_string = str(uuid.uuid4().hex)
    new_image_file_name = f'{unique_string}.{file_ext}'
    destination = Path(os.path.join(STATIC_FILES_DIR, new_image_file_name))
    try:
        with destination.open('wb+') as buffer:
            shutil.copyfileobj(product_image_file.file, buffer)
        return new_image_file_name
    finally:
        product_image_file.file.close()


def create_product_image(db_session: Session, product: models.Product, path: str) -> models.ProductImage:
    product_image = models.ProductImage(
        product_id=product.id,
        path=path,
    )
    db_session.add(product_image)
    db_session.commit()
    return product_image
