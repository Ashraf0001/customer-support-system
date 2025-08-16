import logging
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from app.core.config import settings

"""
Session Module

This module provides a session for database operations.
"""

connection_string = (
    f"postgresql://{settings.database_user}:{settings.database_password}"
    f"@{settings.database_host}:{settings.database_port}/{settings.database_name}"
)
engine = create_engine(connection_string, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def db_session() -> Generator:
    """Database Session Dependency.

    This function provides a database session for each request.
    It ensures that the session is committed after successful operations.
    """
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as ex:
        session.rollback()
        logging.error(ex)
        raise ex
    finally:
        session.close()
