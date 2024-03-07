from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import DonationCharityBase


class Donation(DonationCharityBase):
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        return (
            f'Пожертвование - '
            f'comment={self.comment}, '
            f'user_id={self.user_id}, '
            f'{super().__repr__()}'
        )
