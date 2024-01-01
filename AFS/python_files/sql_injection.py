import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from pprint import pprint
import sys



def get_all_forms(url):
    soup = bs(requests.get(url).content, "html.parser")
    return soup.find_all("form")

def get_form_details(form):
    details = {}
    try:
        action = form.attrs.get("action").lower()
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

def is_vulnerable(response):
    errors = {
        "you have an error in your sql syntax;",
        "warning: mysql",
        "unclosed quotation mark after the character string",
        "quoted string not properly terminated",
        "error in your sql syntax",
        "mysql_fetch_array() expects parameter",
        "mysql_num_rows() expects parameter",
        "mysql_query() expects parameter",
    }
    for error in errors:
        if error in response.content.decode().lower():
            return True
    return False


def scan_sql_injection(url):
    with open("/var/www/AFS/python_files/sql_injection/sql_vectors.txt", "r", encoding="utf-8") as f:
        sql_vectors = f.read().splitlines()

#    vulnerabilities_found = []

#    for vector in sql_vectors:
#        new_url = f"{url}{vector}"
#        res = s.get(new_url)
#        if is_vulnerable(res):
#            print("[+] SQL Injection vulnerability detected, link:", new_url)
#            vulnerabilities_found.append((new_url, vector))
#
    forms = get_all_forms(url)


    for form in forms:
        form_details = get_form_details(form)
        for vector in sql_vectors:
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
            if is_vulnerable(res):
                sql_injection = {}
                sql_injection['success'] = 'O'
                sql_injection['payload'] = repr(vector)[1:-1]
                sql_injection['vuln_url'] = url

                return sql_injection


    sql_injection = {}
    sql_injection['success'] = 'X'
    sql_injection['payload'] = '-'
    sql_injection['vuln_url'] = '-'
    return sql_injection



if __name__ == "__main__":
    if(len(sys.argv)!=2):
        print("Please input argument")
        print("usage: python3 xss.py [url]")
    else:
        try:
            url = sys.argv[1]
            print(scan_sql_injection(url))
        except Exception as e:
            print("[!]Error: " + str(e))

