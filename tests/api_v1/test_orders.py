from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_create_order(client: TestClient, db: Session, account) -> None:
    """Test API POST accounts/1/orders endpoint"""
    data = {
        "timestamp": 157132562,
        "operation": "BUY",
        "issuer_name": "AAPL",
        "total_shares": 2,
        "share_price": 50,
    }
    response = client.post(
        f"/api/v1/accounts/{account.id}/orders",
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert not content["current_balance"]["cash"]
    assert len(content["current_balance"]["issuers"]) == 1
    assert (
        content["current_balance"]["issuers"][0]["issuer_name"] == data["issuer_name"]
    )
    assert (
        content["current_balance"]["issuers"][0]["total_shares"] == data["total_shares"]
    )
    assert (
        content["current_balance"]["issuers"][0]["share_price"] == data["share_price"]
    )
    assert not content["business_errors"]


def test_create_order_missing_value(client: TestClient, db: Session, account) -> None:
    """Test API POST accounts/1/orders endpoint"""
    data = {
        "timestamp": 157132562,
        "issuer_name": "AAPL",
        "total_shares": 2,
        "share_price": 50,
    }
    response = client.post(
        f"/api/v1/accounts/{account.id}/orders",
        json=data,
    )
    assert response.status_code == 422
    content = response.json()
    assert "operation" in content["detail"][0]["loc"]
    assert content["detail"][0]["msg"] == "field required"


def test_create_order_invalid_order(client: TestClient, db: Session, account) -> None:
    """Test API POST accounts/1/orders endpoint"""
    data = {
        "timestamp": 157132562,
        "operation": "BUY",
        "issuer_name": "AAPL",
        "total_shares": 2,
        "share_price": 50,
    }
    response = client.post(
        f"/api/v1/accounts/{0}/orders",
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Account not found"
