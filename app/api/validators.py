from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject

DUPLICATE_NAME = 'Проект с таким именем уже существует!'
NOT_EXIST = 'Проект не найден!'
NOT_ENOUGH = ('Размер необходимых инвестиций {} меньше,'
              'чем текущие инвестиции {} в проекте.')
CLOSED = 'Закрытый проект нельзя редактировать!'
NOT_ZERO = 'В проект были внесены средства, не подлежит удалению!'


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=DUPLICATE_NAME,
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=NOT_EXIST
        )
    return project


def check_invested_amount(invested_amount: int) -> None:
    if invested_amount != 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=NOT_ZERO
        )
    return invested_amount


def check_full_amount(invested_amount: int, full_amount_in: int) -> None:
    if full_amount_in < invested_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=NOT_ENOUGH.format(full_amount_in, invested_amount)
        )
    return full_amount_in


def check_project_closed(fully_invested: bool) -> None:
    if fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=CLOSED
        )
    return fully_invested
