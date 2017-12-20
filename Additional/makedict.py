import re
import requests
import json
from bs4 import BeautifulSoup

def GetText(urlin):
	headers = {
		"Host": "www.dorev.ru",
		"Cookie":"XMMGETHOSTBYADDR213134210163=U1%3A+163.210.unused-addr.ncport.ru; XMMcms4siteUSER=1; XMMFREE=YES; XMMPOLLCOOKIE=XMMPOLLCOOKIE",
		"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
	}
	res = requests.get(urlin, headers=headers)
	Html = res.text

	soup = BeautifulSoup(Html, 'html.parser')
	for table in soup.find_all('table'):
		if 'style' in table.attrs:
			if table['style'] == 'border:1px dotted;border-color:#999999;':
				raw = re.sub('<td></td>',' ',str(table))
				s = BeautifulSoup(raw, 'html.parser')
				T = s.get_text()
				T = T.encode('utf8')
				T = T.decode('utf8')
				T = re.sub(u'\xa0\xa0',r'\n',T)
				T = re.sub(u'\xa0',r'\n',T)
				T = re.sub("'","",T)
				T = T.split('\n')
				Ret = {}
				for i in range(len(T)):
					if i>6:
						splitted = T[i].split(' ')
						if len(splitted)>1 and splitted[0] not in Ret:
							Ret[splitted[0].lower()] = splitted[1].lower()
				return Ret

def buildJSON():
	HtmlString = 'http://www.dorev.ru/ru-index.html?l='
	OutDict = {}
	for i in range(192,224):
		y = GetText(HtmlString+hex(i)[2:])
		OutDict = {**OutDict, **y}
	with open('doref.json', 'w', encoding='utf-8') as outfile:
		json.dump(OutDict, outfile)

buildJSON()



				