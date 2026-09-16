import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import pytest

# Set environment variables before importing settings
os.environ["DATABASE_URL"] = "postgresql://postgres:devpass@localhost:5432/sellince_test"
os.environ["JWT_SECRET_KEY"] = "test-secret-key-do-not-use-in-production"
os.environ["COOKIE_SECURE"] = "False"

TEST_DATABASE_URL = os.environ["DATABASE_URL"]
MAINTENANCE_DATABASE_URL = "postgresql://postgres:devpass@localhost:5432/postgres"

APP_TABLES = [
    "conversations",
    "messages",
    "offers",
    "refresh_tokens",
    "customers",
    "users",
    "companies",
]

CHECKPOINTER_TABLES = [
    "checkpoints",
    "checkpoint_blobs",
    "checkpoint_writes",
]


@pytest.fixture(scope="session", autouse=True)
def _ensure_test_db():
    """Create the sellince_test database once if it does not exist."""
    admin = create_engine(MAINTENANCE_DATABASE_URL, isolation_level="AUTOCOMMIT")
    try:
        with admin.connect() as conn:
            exists = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = 'sellince_test'")
            ).scalar()
            if not exists:
                conn.execute(text("CREATE DATABASE sellince_test"))
    finally:
        admin.dispose()


@pytest.fixture(scope="session")
def test_engine(_ensure_test_db):
    """Create the test engine and initialize the schema."""
    engine = create_engine(TEST_DATABASE_URL)

    from app.core.database import Base
    # Import all models to register them with Base
    from app.models.company import Company
    from app.models.user import User
    from app.models.customer import Customer
    from app.models.conversation import Conversation
    from app.models.message import Message
    from app.models.offer import Offer
    from app.models.refresh_token import RefreshToken

    # Create all tables
    Base.metadata.create_all(bind=engine)
    yield engine

    # Cleanup
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(autouse=True)
def _clean_database(test_engine):
    """Truncate all tables (app + checkpointer) between tests."""
    from sqlalchemy import inspect

    yield
    with test_engine.begin() as conn:
        existing = set(inspect(conn).get_table_names())
        to_truncate = [
            table for table in APP_TABLES + CHECKPOINTER_TABLES if table in existing
        ]
        if to_truncate:
            conn.execute(
                text(
                    "TRUNCATE "
                    + ", ".join(f'"{t}"' for t in to_truncate)
                    + " RESTART IDENTITY CASCADE"
                )
            )


@pytest.fixture
def db_session(test_engine):
    """Create a fresh session for each test."""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(autocommit=False, autoflush=False, bind=connection)()

    yield session

    # Rollback the transaction to clean up after test
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    """Create test client with overridden database dependency."""
    from app.main import app
    from app.core.database import get_db

    app.dependency_overrides[get_db] = lambda: db_session

    with TestClient(app) as test_client:
        yield test_client