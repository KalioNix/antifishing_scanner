import requests
import sys
import re
from bs4 import BeautifulSoup

def check_directory_vulnerability(url):
    vectors_file = "/var/www/AFS/python_files/dir_vector.txt"
    with open(vectors_file, "r", encoding="utf-8") as f:
        vectors = f.read().splitlines()

    directory_listing = {}

    url_parts = url.rstrip('/').split('/')
    
    for i in range(len(url_parts), 0, -1):
        current_url = '/'.join(url_parts[:i]) + '/'  # Construct the URL from the top-level to the current level
        for payload in vectors:
            main_url = current_url + payload
            response = requests.get(main_url)
            if any(vulnerable_keyword in response.text.lower() for vulnerable_keyword in ['index of', 'parent directory', 'directory listing']):
                directory_listing['success'] = 'O'
                directory_listing['payload'] = payload
                directory_listing['vuln_url'] = main_url
                return directory_listing

    # If none of the payloads triggered a vulnerability, return 'X'
    directory_listing['success'] = 'X'
    directory_listing['payload'] = '-'
    directory_listing['vuln_url'] = '-'
    return directory_listing

if __name__ == "__main__":
    if(len(sys.argv) != 2):
        print("Please input argument")
        print("usage: python3 command_injection.py [url]")
    else:
        try:
            url = sys.argv[1]
            result = check_directory_vulnerability(url)
            print(result)
        except Exception as e:
            print("[!]Error: " + str(e))
