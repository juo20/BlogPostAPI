from fastapi.testclient import TestClient
import pytest
from ..main import app
from ..config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..database import Base, get_db
from ..oauth2 import create_access_token


SQLALCHEMY_DATABASE_URL = f"postgresql" \
                          f"://{settings.database_username}" \
                          f":{settings.database_password}" \
                          f"@{settings.database_hostname}" \
                          f":{settings.database_port}" \
                          f"/fastapi_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {
            "name": "test",
            "email": "test@api.com",
            "password": "ilovefastapi"
        }

    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token(data={"email": test_user['email']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture
def test_posts(authorized_client):
    authorized_client.post(
        "/posts/",
        json={
            "title": "First Post",
            "content": "Content"
        }
    )
