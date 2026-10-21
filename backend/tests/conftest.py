
import os
import time

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker


# Set environment variables before importing app settings
os.environ["DATABASE_URL"] = (
    "postgresql://postgres:devpass@localhost:5432/sellince_test"
)
os.environ["JWT_SECRET_KEY"] = "test-secret-key-do-not-use-in-production"
os.environ["COOKIE_SECURE"] = "False"

TEST_DATABASE_URL = os.environ["DATABASE_URL"]

MAINTENANCE_DATABASE_URL = (
    "postgresql://postgres:devpass@localhost:5432/postgres"
)

APP_TABLES = [
    "conversations",
    "messages",
    "offers",
    "refresh_tokens",
    "customers",
    "users",
    "companies",
    "attributions",
]

CHECKPOINTER_TABLES = [
    "checkpoints",
    "checkpoint_blobs",
    "checkpoint_writes",
]


def log_duration(label, start):
    elapsed = time.perf_counter() - start
    print(f"[TEST TIMING] {label}: {elapsed:.2f}s", flush=True)


@pytest.fixture(scope="session", autouse=True)
def _ensure_test_db():
    """Ensure the test database exists."""
    start = time.perf_counter()

    admin = create_engine(
        MAINTENANCE_DATABASE_URL,
        isolation_level="AUTOCOMMIT",
    )

    try:
        with admin.connect() as conn:
            exists = conn.execute(
                text(
                    "SELECT 1 FROM pg_database "
                    "WHERE datname = 'sellince_test'"
                )
            ).scalar()

            if not exists:
                conn.execute(text("CREATE DATABASE sellince_test"))

    finally:
        admin.dispose()
        log_duration("Ensure test database", start)


@pytest.fixture(scope="session")
def test_engine(_ensure_test_db):
    """Create test engine and initialize schema."""
    start = time.perf_counter()

    engine = create_engine(TEST_DATABASE_URL)

    from app.core.database import Base
    from app.models.company import Company
    from app.models.user import User
    from app.models.customer import Customer
    from app.models.conversation import Conversation
    from app.models.message import Message
    from app.models.offer import Offer
    from app.models.refresh_token import RefreshToken
    from app.models.attribution import Attribution

    Base.metadata.create_all(bind=engine)

    log_duration("Create test engine and tables", start)

    yield engine

    start = time.perf_counter()

    Base.metadata.drop_all(bind=engine)
    engine.dispose()

    log_duration("Drop test tables", start)


@pytest.fixture(autouse=True)
def _clean_database(test_engine):
    """Clean app and checkpointer tables before and after each test."""

    def clean_database(stage):
        start = time.perf_counter()

        with test_engine.begin() as conn:
            existing = set(inspect(conn).get_table_names())

            to_truncate = [
                table
                for table in APP_TABLES + CHECKPOINTER_TABLES
                if table in existing
            ]

            if to_truncate:
                conn.execute(
                    text(
                        "TRUNCATE "
                        + ", ".join(f'"{table}"' for table in to_truncate)
                        + " RESTART IDENTITY CASCADE"
                    )
                )

        log_duration(f"Database cleanup ({stage})", start)

    clean_database("before test")

    yield

    clean_database("after test")


@pytest.fixture
def db_session(test_engine):
    """Create a fresh database session for each test."""
    start = time.perf_counter()

    session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
    )()

    log_duration("Create DB session", start)

    yield session

    session.close()


@pytest.fixture
def client(db_session):
    """Create FastAPI test client with overridden database dependency."""
    start = time.perf_counter()

    from app.main import app
    from app.core.database import get_db

    app.dependency_overrides[get_db] = lambda: db_session

    try:
        with TestClient(app) as test_client:
            log_duration("Initialize TestClient", start)
            yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)
