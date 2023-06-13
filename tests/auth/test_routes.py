import pytest
from async_asgi_testclient import TestClient
from fastapi import status
from .get_token import generate_fake_access_token

from src.auth.constants import ErrorCode


@pytest.mark.asyncio
async def test_register(client: TestClient) -> None:
    resp = await client.post(
        "/auth/users",
        json={
            "email": "email@fake.com",
            "password": "123Aa!",
        },
    )
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_201_CREATED
    assert resp_json == {"email": "email@fake.com"}


@pytest.mark.asyncio
async def test_register_email_taken(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    from src.auth.dependencies import service

    async def fake_getter(*args, **kwargs):
        return True

    monkeypatch.setattr(service, "get_user_by_email", fake_getter)

    resp = await client.post(
        "/auth/users",
        json={
            "email": "email@fake.com",
            "password": "123Aa!",
        },
    )
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp_json["detail"] == ErrorCode.EMAIL_TAKEN


@pytest.mark.asyncio
async def test_delete_user(client: TestClient) -> None:
    # Create a dummy user
    create_user_resp = await client.post(
        "/auth/users",
        json={
            "email": "email@fake.com",
            "password": "123Aa!",
        },
    )
    assert create_user_resp.status_code == status.HTTP_201_CREATED

    # Ensure the user was created successfully
    assert create_user_resp.json() == {"email": "email@fake.com"}

    access_token = generate_fake_access_token(user_id=1, is_admin=True)
    delete_user_resp = await client.delete(
        "/auth/delete/user/email@fake.com",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    # Assert the response status code
    assert delete_user_resp.status_code == status.HTTP_200_OK

    # Assert the response JSON or message, if applicable
    assert delete_user_resp.json() == {"detail": "User with 'email@fake.com' deleted successfully"}
