import requests
from bs4 import BeautifulSoup

result = "a_result=`"

url = "https://www.ahnlab.com/kr/site/securityinfo/secunews/secuNewsList.do?curPage=1&menu_dist=1&seq=&key=&dir_group_dist=&dir_code=&searchDate="
url2 = "https://www.ahnlab.com/kr/site/securityinfo/secunews/secuNewsView.do?seq="

titles = []
urls = []
images = []

html = requests.get(url).text

soup = BeautifulSoup(html, 'html.parser') 
lis = soup.select('#secuNewsForm > div > div.listWrap > ul > li ')

for li in lis:
	titles.append(li.select('.tit')[0]['title'])
	urls.append(url2+li.select('input')[0]['value'])

for u in urls:
	html2 = BeautifulSoup(requests.get(u).text, 'html.parser') 
	images.append(html2.select('img')[3]['src'])

for i in range(8):
	result += f'{titles[i]}\n{urls[i]}\n{images[i]}\n\n'
result += "`"


f = open("ahnlab.js", 'w')

f.write(result)
f.close()
