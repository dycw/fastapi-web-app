from pathlib import Path
from typing import Callable
from typing import Optional

import sqlalchemy.orm as orm
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import Session

from fastapi_web_app.data.modelbase import SqlAlchemyBase


__factory: Optional[Callable[[], Session]] = None
__async_engine: Optional[AsyncEngine] = None


def global_init(db_path: Path) -> None:
    global __factory, __async_engine

    if __factory:
        return

    db_file = str(db_path)
    if not db_file or not db_file.strip():
        raise Exception("You must specify a db file.")

    folder = Path(db_file).parent
    folder.mkdir(parents=True, exist_ok=True)

    conn_str = "sqlite:///" + db_file.strip()
    logger.info(f"Connecting to DB with {conn_str}")

    # Adding check_same_thread = False after the recording. This can be an issue about
    # creating / owner thread when cleaning up sessions, etc. This is a sqlite
    # restriction that we probably don't care about in this example.
    engine = create_engine(
        conn_str, echo=False, connect_args={"check_same_thread": False}
    )
    __factory = orm.sessionmaker(bind=engine)

    from fastapi_web_app.data import __all_models  # noqa

    SqlAlchemyBase.metadata.create_all(engine)

    conn_str = "sqlite+aiosqlite:///" + db_file.strip()
    __async_engine = create_async_engine(
        conn_str, echo=False, connect_args={"check_same_thread": False}
    )


def create_session() -> Session:
    global __factory

    if not __factory:
        raise Exception("You must call global_init() before using this method.")

    session: Session = __factory()
    session.expire_on_commit = False

    return session


def create_async_session() -> AsyncSession:
    global __async_engine

    if not __async_engine:
        raise Exception("You must call global_init() before using this method.")

    session: AsyncSession = AsyncSession(__async_engine)
    session.sync_session.expire_on_commit = False

    return session
