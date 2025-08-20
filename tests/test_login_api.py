import requests

def test_login_api():
    url = "https://example.com/api/login"  # 替換為你的 API URL
    payload = {"username": "test_user", "password": "test_pass"}
    response = requests.post(url, json=payload)
    
    assert response.status_code == 200
    assert "token" in response.json()
