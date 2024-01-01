import sys
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pprint import pprint

# Module imports
import requests
from bs4 import BeautifulSoup


# Session setup

def get_all_forms(url):
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    return soup.find_all("form")

def get_form_details(form):
    details = {}
    try:
        action = form.attrs.get("action")
        if action:
            action = action.lower()
    except:
        action = None
    method = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "")
        inputs.append({"type": input_type, "name": input_name, "value": input_value})
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

def is_vulnerable(response, vulnerabilities):
    for vulnerability in vulnerabilities:
        pattern = re.compile(vulnerability, re.IGNORECASE)
        if re.search(pattern, response.text):
            return vulnerability  # 탐지된 취약성 문자열 반환
    return None

def scan_vulnerabilities(url):

    vectors_file = "/var/www/AFS/python_files/command_injection/os_Command.txt"
    vulnerabilities = [
    "command execution error",
    "command not found",
    "invalid command",
    "uid",
    "broadcast",
    "total",
    "Linux",
    "Kali",
    "localhost",
    "nologin",
    "ESTABLISHED"
    ]

    with open(vectors_file, "r", encoding="utf-8") as f:
        vectors = f.read().splitlines()

#    vulnerabilities_found = []

#    for vector in vectors:
#        new_url = f"{url}{vector}"
#        res = s.get(new_url)
##        detected_vulnerability = is_vulnerable(res, vulnerabilities)
#        if detected_vulnerability:
#            print("[+] Vulnerability detected, link:", new_url)
#            vulnerabilities_found.append((new_url, vector, detected_vulnerability))

    forms = get_all_forms(url)
 
    for form in forms:
        form_details = get_form_details(form)
        for vector in vectors:
            data = {}
            for input_tag in form_details["inputs"]:
                if input_tag["type"] == "hidden" or input_tag["value"]:
                    try:
                        data[input_tag["name"]] = input_tag["value"] + vector
                    except:
                        pass
                elif input_tag["type"] != "submit":
                    data[input_tag["name"]] = f"test{vector}"
            url = urljoin(url, form_details["action"])
            if form_details["method"] == "post":
                res = requests.post(url, data=data)
            elif form_details["method"] == "get":
                res = requests.get(url, params=data)
            detected_vulnerability = is_vulnerable(res, vulnerabilities)
            if detected_vulnerability:
                command_injection = {}
                command_injection['success'] = 'O'
                command_injection['payload'] = repr(vector)[1:-1]
                command_injection['vuln_url'] = url

                return command_injection

    command_injection = {}
    command_injection['success'] = 'X'
    command_injection['payload'] = '-'
    command_injection['vuln_url'] = '-'
    return command_injection
    #print(command_injection)





if __name__ == "__main__":
    if(len(sys.argv)!=2):
        print("Please input argument")
        print("usage: python3 command_injection.py [url]")
    else:
        try:
            url = sys.argv[1]
            print(scan_vulnerabilities(url))
        except Exception as e:
            print("[!]Error: " + str(e))
    

