import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from main import app
from app.config.database import get_db
from app.models.sql_models import Base
from app.routers.auth import get_current_user
from unittest.mock import AsyncMock
import os
import asyncio
from sqlalchemy import text

# Test database URL (use absolute path so both setup and app use same file)
TEST_DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "test.db"))
TEST_DATABASE_URL = f"sqlite+aiosqlite:///{TEST_DB_PATH}"

# ensure old test DB is removed
if os.path.exists(TEST_DB_PATH):
    try:
        os.remove(TEST_DB_PATH)
    except OSError:
        pass

engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


@pytest.fixture(scope="session")
def setup_database():
    # Create test database tables (run async code synchronously before tests start)
    async def _create():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(_create())
    yield

    # Drop tables after tests
    async def _drop():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    asyncio.run(_drop())

@pytest.fixture
async def db_session(setup_database):
    async with TestingSessionLocal() as session:
        yield session
        # Clear all tables using DELETE statements
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(f"DELETE FROM {table.name}")
        await session.commit()

@pytest.fixture
def client(setup_database):
    # Provide an async dependency override that yields a fresh async session
    async def override_get_db():
        async with TestingSessionLocal() as session:
            yield session

    # Mock `get_current_user` to return a user with `id=1`
    mock_user = AsyncMock()
    mock_user.id = 1
    mock_user.username = "mockuser"

    app.dependency_overrides[get_current_user] = lambda: mock_user
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    # Clear database after each test
    async def clear_db():
        async with TestingSessionLocal() as session:
            for table in reversed(Base.metadata.sorted_tables):
                await session.execute(text(f"DELETE FROM {table.name}"))
            await session.commit()

    asyncio.run(clear_db())

    # Clear overrides after tests
    app.dependency_overrides.clear()