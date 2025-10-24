import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister():
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # サインアップ
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # 2重登録はエラー
    response_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert response_dup.status_code == 400
    # 削除
    response_del = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response_del.status_code == 200
    assert f"Removed {email}" in response_del.json()["message"]
    # 存在しない参加者削除はエラー
    response_del2 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response_del2.status_code == 400
