from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_returns_message():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "This is an Arabic school!"}


def test_users_protected_requires_auth():
    response = client.get("/users/protected")
    # Should reject when no access token/cookie is provided
    assert response.status_code in (401, 403)


def test_users_get_all_requires_admin():
    response = client.get("/users/")
    # Admin-only route must be unauthorized/forbidden without credentials
    assert response.status_code in (401, 403)


def test_users_create_validation_error_when_body_missing():
    response = client.post("/users/", json={})
    # Pydantic validation should fail
    assert response.status_code == 422


def test_users_login_validation_error_when_body_missing():
    response = client.post("/users/login", json={})
    assert response.status_code == 422


def test_users_logout_returns_message():
    response = client.get("/users/logout")
    assert response.status_code == 200
    assert response.json() == {"message": "User logged out successfully"}


