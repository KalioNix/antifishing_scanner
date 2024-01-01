import requests
from bs4 import BeautifulSoup
import sys

# 세션 생성
s = requests.Session()

def check_vulnerabilities(url):
    response = s.get(url)  # Use the vulnerability URL here
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 모든 input 요소를 찾습니다.
    input_elements = soup.find_all("input")
    
    for input_element in input_elements:
        # input 요소의 name 속성을 확인하고, name이 존재하는 경우에만 값을 대입합니다.
        input_name = input_element.get("name")
        if input_name:
            payload = "A" * 10000  # 대입할 인자값 (10000개의 'A' 문자열)
            
            # POST 요청을 통해 취약점을 확인합니다.
            response = requests.get(url, params={input_name: payload})
            
            # 응답을 분석하여 취약점 여부를 확인합니다.
            if "Error" in response.text or "Request-URI Too Long" in response.text or "Request Entity Too Large " in response.text:
                overflow = {}
                overflow['success'] = 'O'  # 성공 상태 표시
                overflow['payload'] = {input_name}  # 취약한 페이지 정보
                overflow['vuln_url'] = url  # 취약한 URL
                return overflow
    
    # URL 주소 내에 존재하는 파라미터 변수에 많은 인수값을 대입
    for input_element in input_elements:
        input_name = input_element.get("name")
        if input_name:
            payload = "A" * 10000
            
            # URL에 파라미터 추가
            target_url = f"{url}?{input_name}={payload}"
            
            # GET 요청을 통해 취약점을 확인합니다.
            response = s.get(target_url)
            
            # 응답을 분석하여 취약점 여부를 확인합니다.
            if "Error" in response.text or "Request-URI Too Long" in response.text or "Request Entity Too Large " in response.text:
                overflow = {}
                overflow['success'] = 'O'  # 성공 상태 표시
                overflow['payload'] = {input_name}  # 취약한 페이지 정보
                overflow['vuln_url'] = url  # 취약한 URL
                return overflow
    
    # 모든 검사가 완료되었을 때 취약점을 찾지 못한 경우
    overflow = {}
    overflow['success'] = 'X'  # 실패 상태 표시
    overflow['payload'] = '-'  # 취약한 페이지 정보 없음
    overflow['vuln_url'] = '-'  # 취약한 URL 없음
    return overflow

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please input argument")
        print("usage: python3 xss.py [url]")
    else:
        try:
            url = sys.argv[1]
            result = check_vulnerabilities(url)
            print(result)
        except Exception as e:
            print("[!]Error: " + str(e))
