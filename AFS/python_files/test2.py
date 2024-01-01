import sys
import requests
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlencode, urljoin

payloads_file = "redirect_payload.txt"

# 오픈 리다이렉트를 테스트하는 함수
def test_open_redirect(url):
    # HTTP 요청을 보내기 위한 세션 객체를 생성
    s = requests.session()

    # 오픈 리다이렉트를 테스트할 파라미터의 목록
    parameters = ["", "url", "redirect", "go", "goto", "return", "redirect_url", "next"]

    # 주어진 파라미터와 페이로드로 URL을 구성하는 함수
    def construct_payload(url, parameter, payload):
        if parameter == "":
            return url + payload
        else:
            params = {parameter: payload}
            encoded_params = urlencode(params)
            return urljoin(url, "?" + encoded_params)

    # 오픈 리다이렉트를 테스트하는 함수
    def test_redirect(payload):
        
        for parameter in parameters:
            full_url = construct_payload(url, parameter, payload)
            response = s.get(full_url, allow_redirects=False)
            if response.is_redirect:
                redirect = {}
                redirect['success'] = 'O'
                redirect['payload'] = payload
                redirect['vuln_url'] = full_url
                return redirect
            
    results = []  # 결과를 수집할 리스트


    with open(payloads_file, "r", encoding="utf-8") as file:
            payloads = file.readlines()
            with ThreadPoolExecutor() as executor:
                results = executor.map(test_redirect, map(str.strip, payloads))
                for resulta in results:
                    if resulta is not None:
                        # print("[*] 오픈 리다이렉트를 찾았습니다.")
                        return resulta
                # print("[*] 오픈 리다이렉트를 찾지 못했습니다.")
                redirect = {}
                redirect['success'] = 'X'
                redirect['payload'] = '-'
                redirect['vuln_url'] = '-'
                return redirect    


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Please input argument")
        print("usage: python3 xss.py [url]")
    else:
        try:
            url = sys.argv[1]
            result = test_open_redirect(url)
            print(result)
        except Exception as e:
            print("[!]Error: " + str(e))
