from datetime import datetime

from sqlalchemy import Column, Integer, Boolean, DateTime, CheckConstraint

from app.core.config import INVESTED_AMOUNT, FULLY_INVESTED
from app.core.db import Base


class DonationCharityBase(Base):
    __abstract__ = True
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, nullable=False, default=INVESTED_AMOUNT)
    fully_invested = Column(Boolean, nullable=False, default=FULLY_INVESTED)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)
    __table_args__ = (
        CheckConstraint('full_amount > 0'),
        CheckConstraint('invested_amount <= full_amount')
    )

    def __repr__(self):
        return (
            f'<{self.__class__.__name__}, '
            f'(full_amount={self.full_amount}, '
            f'invested_amount={self.invested_amount}, '
            f'fully_invested={self.fully_invested}, '
            f'create_date={self.create_date})>'
        )

    @property
    def remaining_amount(self):
        return self.full_amount - self.invested_amount

    def set_fully_invested(self):
        self.invested_amount = self.full_amount
        self.fully_invested = True
        self.close_date = datetime.now()
