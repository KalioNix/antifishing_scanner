# -*- coding: utf-8 -*-
# 평문 전송 취약점
# login 페이지에서 점검해야함

import requests
import sys
import re
from bs4 import BeautifulSoup


def check_plaintext_transmission(url):
    session = requests.Session()
    
    # 취약점을 점검할 데이터 (평문으로 전송되면 안 되는 민감한 정보)
    data = {'username': 'admin', 'password': 'secretpassword'}

    try:
        response = session.get(url)  # GET 요청을 보냄
        # print("URL : ", url)
        # 응답 확인
        if 'login' in response.text.lower():  # "login"이라는 단어가 응답에 포함되어 있는지 확인
            # 평문으로 데이터를 포함하여 POST 요청을 보냄
            response = session.post(url, data=data)
            if 'admin' in response.text.lower() or 'secretpassword' in response.text.lower():
                # print("[+] 평문 데이터 전송 취약점 발견")
                # print("[!] 응답 내용:")
                # print(response.text)
                plaintext_V = {}
                plaintext_V['success'] = 'O'
                plaintext_V['payload'] = 'detection' #페이로드가 너무 길게 나옴
                plaintext_V['vuln_url'] = url
                return plaintext_V
            else:
                # print("[-] 평문 데이터 전송 취약점 없음")
                plaintext_V = {}
                plaintext_V['success'] = 'X'
                plaintext_V['payload'] = '-'
                plaintext_V['vuln_url'] = '-'
                return plaintext_V
        # else:
        #    print("[-] 폼이 존재하지 않음")

    except requests.exceptions.RequestException as e:
        #print("[-] 요청 오류:", e)
        plaintext_V = {}
        plaintext_V['success'] = 'Error'
        plaintext_V['payload'] = '-'
        plaintext_V['vuln_url'] = '-'
        return plaintext_V

if __name__ == "__main__":
   
    #url = "http://demo.testfire.net/login.jsp"
    #check_plaintext_transmission(session, url)

    if len(sys.argv) != 2:
        print("Please input argument")
        print("usage: python3 xss.py [url]")
    else:
        try:
            url = sys.argv[1]
            result = check_plaintext_transmission(url)
            print(result)
        except Exception as e:
            print("[!]Error: " + str(e))
