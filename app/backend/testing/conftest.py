import pytest
from fastapi.testclient import TestClient
from main import app
from security.redis_client import redis_client


@pytest.fixture(scope="function")
def client():
    return TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def clear_redis():
    """Clear Redis before/after each test (rate limits, cache)."""
    try:
        redis_client.flushdb()
    except Exception:
        pass
    yield
    try:
        redis_client.flushdb()
    except Exception:
        pass
