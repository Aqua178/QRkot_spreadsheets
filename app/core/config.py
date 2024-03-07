from typing import Optional

from pydantic import BaseSettings, EmailStr

INVESTED_AMOUNT = 0
FULLY_INVESTED = False
MAX_LENGTH_NAME = 100
MIN_STR_LENGTH = 1
MAX_LENGTH_DESCRIPTION = 300
TITLE = 'QRKot'
DESCRIPTION = 'Благотворительный фонд поддержки котиков'
DB = 'sqlite+aiosqlite:///./cat_fund.db'
SECRET = 'SECRET'

DRIVE_VERSION = 'v3'
SPREADSHEETS_VERSION = 'v4'

ROW_COUNT = 100
COLUMN_COUNT = 11

UPDATE_RANGE = 'A1:E30'

FORMAT = '%Y/%m/%d %H:%M:%S'


class Settings(BaseSettings):
    app_title: str = TITLE
    description: str = DESCRIPTION
    database_url: str = DB
    secret: str = SECRET
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
