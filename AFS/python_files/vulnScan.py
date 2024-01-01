import sys
from datetime import datetime

from xss import xss
import sql_injection
import adminpage_exposure
import directory_traversal
import unnecessary_methods
import LFI_test
import insecure_communications
import directory_listing
import buffer_overflow
import command_injection
import ldap_injection
import information_leakage
import Plain_Text_Transmission
import open_redirect

import socket
from urllib.parse import urlparse

result = {}

def main(arg):
    result['info'] = {}

    arg = arg.split(',')

    result['info']['url'] = arg[1]
    result['info']['type'] = arg[0]

    now = datetime.now()
    result['info']['start_time'] = now.strftime('%Y-%m-%d %H:%M:%S')

    scan_result = start_scan(arg[2].split('~'))

    now2 = datetime.now()
    result['info']['end_time'] = now2.strftime('%Y-%m-%d %H:%M:%S')
    result['info']['taken_time'] =  str((now2 - now).seconds)

    o = urlparse(arg[1])
    domain = o.hostname
    if domain.startswith('www'):
        domain = domain.replace('www.', '', 1)


    result['info']['ip'] = socket.gethostbyname(domain)

    sys.stdout.write(str(result))





def start_scan(idx):

    for i in idx:
        # XSS
        if i=='0':
            result['0'] = xss.scan_xss(result['info']['url'])
        # SQL Injection
        elif i=='1':
            result['1'] = sql_injection.scan_sql_injection(result['info']['url'])
        # ADMIN page exposure
        elif i=='2':
            result['2'] = adminpage_exposure.check_admin_pages(result['info']['url'])
        # Directory Traversal
        elif i=='3':
            result['3'] = directory_traversal.local_file_inclusion_scanning(result['info']['url'])
        # Unnecessary Methods
        elif i=='4':
            result['4'] = unnecessary_methods.check_unnecessary_methods(result['info']['url'])
        #   File Inclusion
        elif i=='5':
            result['5'] = LFI_test.local_file_inclusion_scanning(result['info']['url'])
        # Insecure Communication
        elif i=='6':
            result['6'] = insecure_communications.check_insecure_communication(result['info']['url'])
        # Directory Listing
        elif i=='7':
            result['7'] = directory_listing.check_directory_vulnerability(result['info']['url'])
        # Buffer_overflow
        elif i=='8':
            result['8'] = buffer_overflow.check_vulnerabilities(result['info']['url'])
        # Command Injection
        elif i=='9':
            result['9'] = command_injection.scan_vulnerabilities(result['info']['url'])
        # LDAP Injection
        elif i=='10':
            result['10'] = ldap_injection.scan_ldap_injection(result['info']['url'])
        # Information Leakage
        elif i=='11':
            result['11'] = information_leakage.main(result['info']['url'])
        # Plain Text Transmission
        elif i=='12':
            result['12'] = Plain_Text_Transmission.check_plaintext_transmission(result['info']['url'])
        # Open Redirect
        elif i=='13':
            result['13'] = open_redirect.test_open_redirect(result['info']['url'])

	
            
    return str(result)

    


if __name__ == '__main__':
    main(sys.argv[1])
    #sys.stdout.write(main("quickscan,http://118.67.131.9:8080/AFS/index.html,0 1 3 5"))


'''
{
  info : {
    url : https://naver.com,
    type : quickscan,
    start_time : yyyy-mm-dd hh-mm-ss,
    end_time : yyyy-mm-dd hh-mm-ss,
    taken_time : 100m
  },
  0 : {
    success : O,
    payload : <script>alert(1);</script>
    vuln_url : https://naver.com/login.html
  }
}


arg -> "quickscan,https://www.naver.com,0 1 3 5"
'''
