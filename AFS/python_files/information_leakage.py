import requests
import sys

def main(url):
    
    url_404 = url + "404error"

    #print("점검 URL : " + str(url_404))


    response = requests.get(url_404)
    status = response.status_code
    res = response.text
    #print('에러 코드 : ' + str(status))


    res = res.lower()
    if 'apache' in res or 'tomcat' in res:
        #data = "점검 결과 : 취약(apache 또는 tomcat을 발견함)"
        leakage = {}
        leakage['success'] = 'O'  # 성공 상태 표시
        leakage['payload'] = 'apache or tomcat'  # 페이로드
        leakage['vuln_url'] = url  # 취약한 URL
        return leakage
    elif 'jboss web' in res:
        #data = "점검 결과 : 취약(jboss web을 발견함)"
        leakage = {}
        leakage['success'] = 'O'  # 성공 상태 표시
        leakage['payload'] = 'jboss web'  # 페이로드
        leakage['vuln_url'] = url  # 취약한 URL
        return leakage
    elif 'nginx' in res:
        #data = "점검 결과 : 취약(nginx를 발견함)"
        leakage = {}
        leakage['success'] = 'O'  # 성공 상태 표시
        leakage['payload'] = 'nginx'  # 페이로드
        leakage['vuln_url'] = url  # 취약한 URL
        return leakage
    elif 'resin' in res:
        #data = "점검 결과 : 취약(resin을 발견함)"
        leakage = {}
        leakage['success'] = 'O'  # 성공 상태 표시
        leakage['payload'] = 'resin'  # 페이로드
        leakage['vuln_url'] = url  # 취약한 URL
        return leakage
    elif 'ibm_http_server' in res:
        #data = "점검 결과 : 취약(ibm_http_server를 발견함)"
        leakage = {}
        leakage['success'] = 'O'  # 성공 상태 표시
        leakage['payload'] = 'ibm_http_server'  # 페이로드
        leakage['vuln_url'] = url  # 취약한 URL
        return leakage
    elif 'jspg0036e' in res:
        #data = "점검 결과 : 취약(jspg0036e를 발견함)"
        leakage = {}
        leakage['success'] = 'O'  # 성공 상태 표시
        leakage['payload'] = 'jspg0036e'  # 페이로드
        leakage['vuln_url'] = url  # 취약한 URL
        return leakage
    elif 'rfc 2068' in res:
        #data = "점검 결과 : 취약(RFC 2068를 발견함)"
        leakage = {}
        leakage['success'] = 'O'  # 성공 상태 표시
        leakage['payload'] = 'RFC 2068'  # 페이로드
        leakage['vuln_url'] = url  # 취약한 URL
        return leakage
    else:
        #data = "점검 결과 : 양호"
        leakage = {}
        leakage['success'] = 'X'  
        leakage['payload'] = '-' 
        leakage['vuln_url'] = '-'
        return leakage
    #print(data)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please input argument")
        print("usage: python3 xss.py [url]")
    else:
        try:
            url = sys.argv[1]
            result = main(url)
            print(result)
        except Exception as e:
            print("[!]Error: " + str(e))
