# 불필요한 HTTP 메소드 취약점 점검
# GET과 POST를 제외한 나머지 메소드가 사용되는지 점검
# 존재한다면 출력함

import requests
import sys

def check_unnecessary_methods(url):
    methods = ['PUT', 'DELETE', 'TRACE', 'OPTIONS', 'CONNECT']
    unnecessary_methods = []
    
    for method in methods:
        response = requests.request(method, url)
        # HTTP 응답이 성공한 경우에만
        if response.status_code == 200:
            unnecessary_methods.append(method)
    
    if len(unnecessary_methods) > 0:
        redirect = {}
        redirect['success'] = 'O'
        redirect['payload'] = ', '.join(unnecessary_methods)
        redirect['vuln_url'] = url
        return redirect
    else:
        redirect = {}
        redirect['success'] = 'X'
        redirect['payload'] = '-'
        redirect['vuln_url'] = '-'
        return redirect



if __name__ == "__main__":
    if(len(sys.argv)!=2):
        print("Please input argument")
        print("usage: python3 command_injection.py [url]")
    else:
        try:
            url = sys.argv[1]
            print(check_unnecessary_methods(url))
        except Exception as e:
            print("[!]Error: " + str(e))
    

