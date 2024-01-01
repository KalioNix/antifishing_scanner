import requests
import re
import json
import socket
import sys

criminal_api_key = "UVUY39KrwS1bi4G3fAwzxWLQDeFEJ5Xy3POAiDlmigNWITMORV7kA06XT2xB"
gonggong_data_key =  "SDtKAomEaycQLYC8%2BllD4XsPYPpmUtPMwGh08a759cSrFL7o%2By1rv5%2FzqU9TCjpKcmWcbkzeWcnaIF7c%2BE7CUA%3D%3D"

# 05.01 url에서 domain name만 가져오는 정규표현식 작성해야함
base_url = "https://api.criminalip.io/v1/domain/reports?query="

ip_summary_url = "https://api.criminalip.io/v1/ip/summary?ip=" #05.03 url을 http,www 없이 입력 했을 때 대책 만들어야 함 ip_data API url
malicious_url = "https://api.criminalip.io/v1/feature/ip/malicious-info?ip=" #malicious-info API url

result = ""
plus = 0

def parse_domain(url) :
    from urllib.parse import urlparse
    o = urlparse(url)
    domain = o.hostname
    if domain.startswith('www'):
        domain = domain.replace('www.', '', 1)

    return domain

def change_domain_ip(x) :

    ip = socket.gethostbyname(x)
    #print(ip)
    global result
    result += ";"
    result += ip
    return ip


def check_dns_safety(domain):  # 05.01 check_dns_safety 함수 생성,  아직은 Dangerous만 구현

    url = f"{base_url}{domain}"
    payload = {}
    headers = {"x-api-key": criminal_api_key}

    do_response = requests.get(url, headers=headers)



    if do_response.status_code == 200:

        doamin_re_data = do_response.json()

        #https://www.naver.com/scan_id = doamin_re_data['data']['reports'][0]['scan_id']

        score = doamin_re_data['data']['reports'][0]['score']

        if score == "Critical":
            print(f"{domain}은(는) 매우 위험합니다!!")
        elif score == "Dangerous":
            print(f"{domain}은(는) 위험합니다!!")
        elif score == "Moderate" :
            print(f"{domain}은(는) 주의할 필요가 있어요.")
        elif score == "Low":
            print(f"{domain}은(는) 괜찮아요.")
        elif score == "Safe":
            print(f"{domain}은(는) 안전한 사이트에요.")


def check_ip_safe(ip) : # IP 점수와 국가 코드 반환
    url = f"{ip_summary_url}{ip}"
    payload = {}
    headers = {"x-api-key": criminal_api_key}

    ip_response = requests.get(url, headers=headers)


    if ip_response.status_code == 200 :
        ip_re_data = ip_response.json()

        inbound_score = ip_re_data['score']['inbound']
        outbound_score = ip_re_data['score']['outbound']

        score = inbound_score * 10 + outbound_score*10
        country_code = ip_re_data['country_code']
        #print("80점 이상 : 안전, 60점 이상 : 보통, 40점 이상 : 경고, 20점 이하 : 위험 ")
        #print(f"점수 = {100 - score} 점")
        #print(f"나라 코드 : {country_code}")
        global result
        result += ";" + str(100-score) + ";" + country_code.upper()

        return score, country_code


# def malicious_info(ip) :
#      url = f"{malicious_url}{ip}"
#      payload = {}
#      headers = {"x-api-key": criminal_api_key}
#      malicious_response = requests.get(url, headers=headers)
#
#      if malicious_response.status_code == 200:
#         mal_re_data = malicious_response.json()
#
#         return malicious_response.text

def whois_check(domain): #KISA WHOIS 등록 정보 확인 def
    whois_api_url = f"http://apis.data.go.kr/B551505/whois/domain_name?serviceKey={gonggong_data_key}&query={domain}&answer=json"

    whois_response = requests.get(whois_api_url)
    # data = json.loads(whois_response)
    # print(data)
    whois_data = whois_response.json()
    result_code = whois_data['response']['result']['result_code']

    global result
    global plus
    if result_code == '10000':
        #print("한국인터넷진흥원 등록 도메인입니다.")
        result += ";한국인터넷진흥원 등록 도메인입니다."
        plus = 10
    else :
        #print("한국인터넷진흥원에는 없는 도메인입니다.")
        result += ";한국인터넷진흥원에는 없는 도메인입니다."


def open_port(ip) :
   url = f"{malicious_url}{ip}"
   payload = {}
   headers = {"x-api-key": criminal_api_key}
   
   malicious_response = requests.get(url, headers=headers)
   global result
   
   
   
   if malicious_response.status_code == 200:
      mal_re_data = malicious_response.json()
      count = mal_re_data['current_opened_port']['count']
      port_num = []
      i=0
      for i in range(count):
        value = mal_re_data['current_opened_port']['data'][i]['port']
        i = i+1
        port_num.append(value)
        res = ', '.join(str(port) for port in port_num)
   
   result += f";{res}"#count == 열린 포트 개수, port_num == 포트 번호
   




if __name__ == "__main__":
    if(len(sys.argv)!=2):
        pass
    else:
        try:
            x = sys.argv[1]
            result += x
            changed_domain = parse_domain(x)
            whois_check(changed_domain)
            ip = change_domain_ip(changed_domain)
            score, country_code = check_ip_safe(ip) #05.03 url에서 domain name만 가져와 ip로 바꾸고 inbound, outbound 점수 출력하는 것과 domain score 출력까지 완성
            score += plus
            if score > 100:
                score=100
            open_port(ip)
            sys.stdout.write(result)
        except Exception as e:
            print(e)

# mal = malicious_info(ip)
# print(f"{mal}")
