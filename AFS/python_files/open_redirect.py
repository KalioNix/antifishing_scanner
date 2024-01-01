import sys
import requests
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlencode, urljoin

# payloads_file = "redirect_payload.txt"

# 오픈 리다이렉트를 테스트하는 함수
def test_open_redirect(url):
    
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
