from sqlalchemy import Column, String

from app.core.config import MAX_LENGTH_NAME, MAX_LENGTH_DESCRIPTION
from app.models.base import DonationCharityBase


class CharityProject(DonationCharityBase):
    name = Column(String(MAX_LENGTH_NAME), unique=True, nullable=False)
    description = Column(String(MAX_LENGTH_DESCRIPTION), nullable=False)

    def __repr__(self):
        return (
            f'Проект - '
            f'name={self.name}, '
            f'description={self.description}, '
            f'{super().__repr__()}'
        )
