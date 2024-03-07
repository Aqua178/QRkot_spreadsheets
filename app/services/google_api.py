from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', settings.DRIVE_VERSION)
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        )
    )


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(settings.FORMAT)

    service = await wrapper_services.discover('sheets', settings.SPREADSHEETS_VERSION)

    spreadsheet_body = {
        'properties': {'title': f'Отчёт от {now_date_time}',
                       'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': 'Лист1',
                                   'gridProperties': {'rowCount': settings.ROW_COUNT,
                                                      'columnCount': settings.COLUMN_COUNT}}}]
    }

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheet_id']


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(settings.FORMAT)
    service = await wrapper_services.discover('sheets', settings.SPREADSHEETS_VERSION)

    table_values = [
        ['Отчёт от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание'],
    ]

    for project in projects:
        new_row = [
            project.name,
            str(project.close_date - project.create_date),
            project.description,
        ]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheet_id=spreadsheet_id,
            range=settings.UPDATE_RANGE,
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
