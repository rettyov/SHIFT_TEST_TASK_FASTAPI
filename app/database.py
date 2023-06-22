from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


from private_db_settings import Settings


setting: Settings = Settings()
setting.init_variables()

SQLALCHEMY_DATABASE_URL = f'postgresql://{setting.POSTGRES_USER}:{setting.POSTGRES_PASSWORD}' \
                           f'@{setting.HOST_DB}:{setting.PORT}/{setting.POSTGRES_DB}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
