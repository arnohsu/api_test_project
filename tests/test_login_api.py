import requests

def test_login_api():
    # 使用 ReqRes 提供的公開登入 API
    url = "https://reqres.in/api/login"
    payload = {"email": "eve.holt@reqres.in", "password": "cityslicka"}
    
    response = requests.post(url, json=payload)

    print("Status Code:", response.status_code)
    print("Response Body:", response.text)

    # 驗證回傳狀態碼是否正確
    assert response.status_code == 200
    # 驗證回傳是否包含 token
    assert "token" in response.json()
