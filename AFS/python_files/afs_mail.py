import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication 
from email.header import Header
from email.mime.text import MIMEText
import sys
import base64
import urllib.parse


def mail_send(mail_item):

    split_text = base64_decode_string(mail_item).split('***')
          	
	
    SECRET_ID = "inbo_afs"
    SECRET_PASS = "1q2w3e4r!"
    
    try:
        smtp = smtplib.SMTP('smtp.naver.com',587)
        smtp.ehlo() 
        smtp.starttls()#TLS 사용시 필요

        smtp.login(SECRET_ID, SECRET_PASS)

        myemail = "inbo_afs@naver.com"
        youremail = "inbo_afs@naver.com"
        content_msg = f"""이름 : {split_text[0]}
        \n 이메일 : {split_text[1]}
        \n 내용 : {split_text[3]}"""
        msg = MIMEText(content_msg.encode('utf-8'), _subtype='plain', _charset='utf-8')
        msg['Subject'] = Header(split_text[2].encode('utf-8'), 'utf-8')
        msg['From'] = myemail
        msg['To'] = youremail
        
        smtp.sendmail(myemail,youremail,msg.as_string())
        smtp.quit()
        print("success")
    except:
        print("fail")


#인코딩
def base64_encode_string(input_string) :
    encoded_bytes =base64.b64encode(input_string.encode('utf-8'))
    encoded_string = encoded_bytes.decode('utf-8')
    return encoded_string

#디코딩
# JavaScript의 atob 함수와 동일한 파이썬 함수
def atob(s):
    return base64.b64decode(s).decode('utf-8')

def base64_decode_string(encoded_string) : 
    decoded_url = urllib.parse.unquote(encoded_string)
    decoded_string = atob(decoded_url)
    return decoded_string





if __name__ == "__main__":
    if(len(sys.argv)!=2):
        print("Please input argument")
        print("usage: python3 command_injection.py [url]")
    else:
        try:
            text = sys.argv[1]
            mail_send(text)
            
        except Exception as e:
            print("[!]Error: " + str(e))


