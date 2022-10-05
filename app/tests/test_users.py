from .. import schemas
from jose import jwt
from ..config import settings
import pytest


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "name": "test",
            "email": "test@api.com",
            "password": "ilovefastapi"
        },
    )

    new_user = schemas.ResponseUser(**response.json())
    assert response.status_code == 201
    assert new_user.email == "test@api.com"


def test_login_user(client, test_user):
    response = client.post(
        "/login",
        data={
            "username": test_user['email'],
            "password": test_user['password']
        },
    )
    assert response.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('jan@gmail.com', 'maslotohaslo', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('jan@gmail.com', None, 422)
])
def test_failed_login(client, test_user, email, password, status_code):
    response = client.post(
        "/login",
        data={
            "username": email,
            "password": password
        },
    )

    assert response.status_code == status_code


def test_token(client, test_user):

    SECRET_KEY = f"{settings.secret_key}"
    ALGORITHM = f"{settings.algorithm}"

    response = client.post(
        "/login",
        data={
            "username": test_user['email'],
            "password": test_user['password']
        },
    )

    token = schemas.Token(**response.json())
    payload = jwt.decode(token.access_token, SECRET_KEY, algorithms=[ALGORITHM])
    email: str = payload.get("email")

    assert response.status_code == 200
    assert email == test_user['email']
    assert token.token_type == "bearer"
