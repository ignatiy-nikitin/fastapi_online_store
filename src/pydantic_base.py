from pydantic import BaseModel


class BasePDModel(BaseModel):
    """Base Pydantic model."""

    class Config:
        orm_mode = True
