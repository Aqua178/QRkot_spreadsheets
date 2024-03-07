from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, Extra

from app.core.config import (MAX_LENGTH_NAME, MAX_LENGTH_DESCRIPTION,
                             MIN_STR_LENGTH)


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(max_length=MAX_LENGTH_NAME)
    description: Optional[str] = Field(max_length=MAX_LENGTH_DESCRIPTION)
    full_amount: Optional[PositiveInt]

    class Config():
        extra = Extra.forbid
        BaseModel.Config.min_anystr_length = MIN_STR_LENGTH


class CharityProjectCreate(BaseModel):
    name: str = Field(max_length=MAX_LENGTH_NAME)
    description: str = Field(max_length=MAX_LENGTH_DESCRIPTION)
    full_amount: PositiveInt


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
