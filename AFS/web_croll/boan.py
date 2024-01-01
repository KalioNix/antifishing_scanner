import requests
from bs4 import BeautifulSoup
import ssl


ssl._create_default_https_context = ssl._create_unverified_context
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
result = "b_result=`"

url = "https://www.boannews.com/media/t_list.asp"
#url2 = "https://www.ahnlab.com/kr/site/securityinfo/secunews/secuNewsView.do?seq="

titles = []
urls = []
images = []

html = requests.get(url,verify=False).text

soup = BeautifulSoup(html, 'html.parser') 
lis = soup.select('.news_list')

for li in lis:
	titles.append(li.select('.news_txt')[0].text)

	if li.select('img'):
		images.append("https://www.boannews.com" + li.select('img')[0]['src'])
	else:
		images.append('No_Image')


	urls.append("https://www.boannews.com" + li.select('a')[0]['href'])

for i in range(8):
	result += f'{titles[i]}\n{urls[i]}\n{images[i]}\n\n'
result += "`"


f = open("boan.js", 'w')

f.write(result)
f.close()





