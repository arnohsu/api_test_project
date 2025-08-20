import requests

def test_login_api():
    # 用 httpbin.org 測試 POST，會直接回傳你送的資料
    url = "https://httpbin.org/post"
    payload = {"username": "test_user", "password": "test_pass"}

    response = requests.post(url, json=payload)

    print("Status Code:", response.status_code)
    print("Response Body:", response.json())

    # 驗證 200 OK
    assert response.status_code == 200
    # 驗證回傳有你送出的資料
    json_data = response.json()
    assert json_data["json"]["username"] == "test_user"
    assert json_data["json"]["password"] == "test_pass"
