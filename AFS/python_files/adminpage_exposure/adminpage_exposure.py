# 관리자 페이지 노출 취약점
# 검사 방법중 하나는 구글에서 inurl:admin 검색하면 노출되는 페이지
# 검사 목록이 너무 많아서 자주 사용되는 것들만 추림. 

import requests
import time
import sys

admin_pages = [
    "/setup/",
    "/admin/",
    "/administrator/",
    "/login/",
    "/webmaster/",
    "/adminlogin/",
    "/adminpanel/",
    "/admin.php/",
    "/admin.html/",
    "/admin.asp/",
    "/admin.jsp/",
    "/admin.aspx/",
    "/admin.cfm/",
    "/admin.cgi/",
    "/admin.pl/",
    "/admin.py/",
    "/adm/",
    "/manage/",
    "/manager/",
    "/backend/",
    "/login_adm/",
    "/master/",
    "/control/",
    "/system/",
    "/console/",
    "/cms/",
    "/wp-admin/",
    "/joomla/administrator/",
    "/drupal/admin/",
    "/magento/admin/",
    "/prestashop/admin/",
    "/vbulletin/admincp/",
    "/phpmyadmin/",
    "/pma/",
    "/mysql/",
    "/sql/",
    "/admin_login/",
    "/admin_area/",
    "/adm1n/",
    "/adm1n1strator/",
    "/admin123/",
    "/admin1234/",
    "/1admin/",
    "/admin_test/",
    "/setup.php/"
]

find_admin = []

def check_admin_pages(url):
    # admin_pages의 각 페이지를 검사
    for page in admin_pages:
        full_url = url + page
        res = requests.get(full_url)
        if res.status_code == 200:
            # 취약점 발견 시 해당 정보 반환
            redirect = {}
            redirect['success'] = 'O'  # 성공 상태 표시
            redirect['payload'] = page  # 취약한 페이지 정보
            redirect['vuln_url'] = url  # 취약한 URL
            return redirect
        elif res.status_code != 404:
            pass

    # URL 경로를 줄여가며 다시 검사
    for i in range(len(url.split('/')) - 1, 2, -1):
        reduced_url = '/'.join(url.split('/')[:i]) + '/'
        for page in admin_pages:
            full_url = reduced_url + page
            res = requests.get(full_url)
            if res.status_code == 200:
                # 취약점 발견 시 해당 정보 반환
                redirect = {}
                redirect['success'] = 'O'  # 성공 상태 표시
                redirect['payload'] = page  # 취약한 페이지 정보
                redirect['vuln_url'] = reduced_url  # 취약한 URL
                return redirect
            elif res.status_code != 404:
                pass

    # 취약점을 발견하지 못한 경우
    redirect = {}
    redirect['success'] = 'X'  # 실패 상태 표시
    redirect['payload'] = '-'  # 취약한 페이지 정보 없음
    redirect['vuln_url'] = '-'  # 취약한 URL 없음
    return redirect

# 취약점 검사 실행


if __name__ == "__main__":
    if(len(sys.argv)!=2):
        print("Please input argument")
        print("usage: python3 command_injection.py [url]")
    else:
        try:
            url = sys.argv[1]
            check_admin_pages(url)
        except Exception as e:
            print("[!]Error: " + str(e))
    

