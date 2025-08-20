cat > tests/test_login_api.py << 'EOF'
import requests  # 送 HTTP 請求

def test_login_api_success():
    url = "https://reqres.in/api/login"                     # 測試 API
    payload = {"email": "eve.holt@reqres.in", "password": "cityslicka"}  # 正確帳密
    r = requests.post(url, json=payload)                    # POST
    assert r.status_code == 200                             # 驗證 200
    assert "token" in r.json()                              # 回傳需帶 token

def test_login_api_fail():
    url = "https://reqres.in/api/login"
    payload = {"email": "peter@klaven"}                     # 少了 password
    r = requests.post(url, json=payload)
    assert r.status_code == 400                             # 驗證 400
    assert "error" in r.json()                              # 回傳需帶 error
EOF
