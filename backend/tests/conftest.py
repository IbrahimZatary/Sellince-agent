import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite:///./test_database.db"


@pytest.fixture(scope="session")
def test_engine():
    """Create test engine and initialize schema."""
    if os.path.exists("./test_database.db"):
        try:
            os.remove("./test_database.db")
        except PermissionError:
            pass

    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )

    from app.models.company import Company
    from app.models.user import User
    from app.models.customer import Customer
    from app.models.conversation import Conversation
    from app.models.message import Message
    from app.models.offer import Offer
    from app.models.refresh_token import RefreshToken

    Base.metadata.create_all(bind=engine)
    yield engine

    Base.metadata.drop_all(bind=engine)
    engine.dispose()

    if os.path.exists("./test_database.db"):
        try:
            os.remove("./test_database.db")
        except PermissionError:
            pass


@pytest.fixture(scope="function")
def db_session(test_engine):
    """Provide a dedicated database session for a test function."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture(scope="function")
def client(test_engine):
    """Provide a FastAPI TestClient bound to a fresh test DB session per request."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

    # Clean data between test functions
    from app.core.database import Base
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
