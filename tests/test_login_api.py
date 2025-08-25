import requests

def test_login_api():
    url = "https://httpbin.org/post"
    payload = {"username": "test_user", "password": "test_pass"}

    response = requests.post(url, json=payload)

    print("Status Code:", response.status_code)
    try:
        data = response.json()
        print("Response Body:", data)
        assert response.status_code == 200
        assert data["json"]["username"] == "test_user"
    except Exception as e:
        print("Response is not JSON:", response.text)
        assert False, f"API call failed: {e}"
