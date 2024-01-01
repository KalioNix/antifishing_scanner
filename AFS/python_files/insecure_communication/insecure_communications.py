import requests
import sys

def check_insecure_communication(url):
    # http:// 또는 https://가 포함된 URL이 아닌 경우, 자동으로 https:// 프로토콜을 추가
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    
    response = requests.get(url)
    # HTTPS 프로토콜을 사용하지 않는 경우
    if response.history and response.history[0].status_code == 301:
        insecure_communication= {}
        insecure_communication['success'] = 'O'
        insecure_communication['payload'] = 'HTTPS 대신 HTTP를 사용합니다'
        insecure_communication['vuln_url'] = url
        return insecure_communication
    # SSL/TLS 구성에 문제가 있는 경우
    elif response.status_code == 200 and not response.url.startswith("https"):
        insecure_communication= {}
        insecure_communication['success'] = 'O'
        insecure_communication['payload'] = 'SSL/TLS 구성 문제가 있습니다'
        insecure_communication['vuln_url'] = url
        return insecure_communication
    # 안전한 통신을 사용하는 경우
    else:
        insecure_communication= {}
        insecure_communication['success'] = 'X'
        insecure_communication['payload'] = '-'
        insecure_communication['vuln_url'] = '-'
        return insecure_communication


if __name__ == "__main__":
    if(len(sys.argv)!=2):
        print("Please input argument")
        print("usage: python3 command_injection.py [url]")
    else:
        try:
            url = sys.argv[1]
            check_insecure_communication(url)
        except Exception as e:
            print("[!]Error: " + str(e))
