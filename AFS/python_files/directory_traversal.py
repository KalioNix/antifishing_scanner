import requests
import sys
import re
from bs4 import BeautifulSoup


def local_file_inclusion_scanning(url):

    vectors_file = "/var/www/AFS/python_files/directory_traversal/traversal_vector.txt"
    with open(vectors_file, "r", encoding="utf-8") as f:
        vectors = f.read().splitlines()

    vulnerability_found = False  # Flag to keep track of vulnerability status

    for payload in vectors:
        main_url = url + payload
        response = requests.get(main_url)
        #print(response.status_code)

        if any(vulnerable_keyword in response.text for vulnerable_keyword in ["root", "www-data", "/usr/bin/zsh", "/usr/bin/bash", "0:0"]):
            directory_traversal = {}
            directory_traversal['success'] = 'O'
            directory_traversal['payload'] = payload
            directory_traversal['vuln_url'] = main_url
            return directory_traversal
        elif response.status_code == 200 and "root:x" in response.text:
            directory_traversal = {}
            directory_traversal['success'] = 'O'
            directory_traversal['payload'] = payload
            directory_traversal['vuln_url'] = main_url
            return directory_traversal

    directory_traversal = {}
    directory_traversal['success'] = 'X'
    directory_traversal['payload'] = '-'
    directory_traversal['vuln_url'] = '-'
    return directory_traversal





if __name__ == "__main__":
    if(len(sys.argv)!=2):
        print("Please input argument")
        print("usage: python3 command_injection.py [url]")
    else:
        try:
            url = sys.argv[1]
            result = local_file_inclusion_scanning(url)
            print(result)
        except Exception as e:
            print("[!]Error: " + str(e))
    


