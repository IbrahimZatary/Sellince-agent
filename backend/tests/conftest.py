import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import pytest

# Set environment variables before importing settings
os.environ["DATABASE_URL"] = "sqlite:///./test_database.db"
os.environ["JWT_SECRET_KEY"] = "test-secret-key-do-not-use-in-production"
os.environ["COOKIE_SECURE"] = "False"

# Use file-based test database
TEST_DATABASE_URL = "sqlite:///./test_database.db"


@pytest.fixture(scope="session")
def test_engine():
    """Create test engine and initialize schema"""
    # Remove existing test database
    if os.path.exists("./test_database.db"):
        os.remove("./test_database.db")
    
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
    
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
    if os.path.exists("./test_database.db"):
        os.remove("./test_database.db")


@pytest.fixture
def db_session(test_engine):
    """Create a fresh session for each test"""
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
    """Create test client with overridden database dependency"""
    from app.main import app
    from app.core.database import get_db

    app.dependency_overrides[get_db] = lambda: db_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
