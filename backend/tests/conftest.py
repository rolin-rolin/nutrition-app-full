import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest

from app.db.session import SessionLocal


@pytest.fixture()
def db():
    """Provide a database session for tests."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()