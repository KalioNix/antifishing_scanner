import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from pprint import pprint

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
}

def get_all_forms(soup):
    forms = soup.find_all("form")
    forms += soup.find_all("input", {"type": "submit", "form": True})
    
    # 추가: hidden input 태그의 부모 폼 찾기
    hidden_inputs = soup.find_all("input", {"type": "hidden"})
    for input_tag in hidden_inputs:
        parent_form = input_tag.find_parent("form")
        if parent_form not in forms:
            forms.append(parent_form)
    
    return forms



def get_form_details(form):
    details = {}
    action = form.attrs.get("action") if form and form.attrs else None
    method = form.attrs.get("method", "get").lower() if form and form.attrs else "get"
    inputs = []
    
    if form:
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
    session = requests.Session()
    session.headers.update(HEADERS)

    with open("sql_vectors.txt", "r", encoding="utf-8") as f:
        sql_vectors = f.read().splitlines()

    vulnerabilities_found = []

    response = session.get(url)
    soup = bs(response.content, "html.parser")

    for vector in sql_vectors:
        new_url = f"{url}{vector}"
        print("[!] Trying", vector)
        res = session.get(new_url)
        if is_vulnerable(res):
            vulnerabilities_found.append((new_url, vector))

    forms = get_all_forms(soup)
    print("--------------------------------------------------------------------------")
    print(f"[+] Detected {len(forms)} forms on {url}.")
    print("--------------------------------------------------------------------------")

    for form in forms:
        form_details = get_form_details(form)
        for vector in sql_vectors:
            data = {}
            for input_tag in form_details["inputs"]:
                if input_tag["type"] == "hidden" or input_tag["value"]:
                    try:
                        data[input_tag["name"]] = input_tag["value"] + vector
                    except KeyError:
                        pass
                elif input_tag["type"] != "submit":
                    data[input_tag["name"]] = f"test{vector}"
            form_action = urljoin(url, form_details["action"])
            if form_details["method"] == "post":
                res = session.post(form_action, data=data)
            elif form_details["method"] == "get":
                res = session.get(form_action, params=data)
            if is_vulnerable(res):
                vulnerabilities_found.append((form_action, vector))

    if len(vulnerabilities_found) == 0:
        print("[-] No SQL Injection vulnerabilities detected.")
    else:
        print("[+] Vulnerabilities found with payloads:")
        for vuln_url, payload in vulnerabilities_found:
            print(f"   - URL: {vuln_url}")
            print(f"     Payload: {payload}")
            print("[+] Form:")
            pprint(form_details)

    print("--------------------------------------------------------------------------")
    print("[+] Total SQL Injection vulnerabilities found:", len(vulnerabilities_found))
    print("--------------------------------------------------------------------------")

if __name__ == "__main__":
    #url = "http://118.67.131.9:8080/AFS/contact.html"
    url = "http://testphp.vulnweb.com/login.php"
    scan_sql_injection(url)
