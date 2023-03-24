from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_create_account(client: TestClient, db: Session) -> None:
    """Test API POST accounts/ endpoint"""
    data = {"cash": 100}
    response = client.post(
        "/api/v1/accounts/",
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["cash"] == 100
    assert "id" in content
