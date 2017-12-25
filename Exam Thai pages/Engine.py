import json
import urllib
import os

from bs4 import BeautifulSoup

from flask import Flask
from flask import render_template
from flask import request

def Dictionarize():
	Dict = {}
	
	for file in os.listdir('thai_pages'):
		with open('thai_pages'+os.sep+file,'r',encoding='utf-8') as html:
			h = html.read()
			soup = BeautifulSoup(h, 'html.parser')
			data = []
			table = soup.find('table', attrs={'class':'gridtable'})
			# print(table.get_text())
			table_body = table
			rows = table_body.find_all('tr')
			for row in rows:
				cols = row.find_all('td')
				cols = [ele.text.strip() for ele in cols]
				data.append([ele for ele in cols]) #  if ele
			
			for row in data:
				if len(row) == 4:
					Dict[row[0]] = row[3].split(';')[0]
	return Dict

def jsonize(indict):
	with open('THA_to_ENG.json','w',encoding='utf-8') as thatoeng:
		json.dump(indict, thatoeng, ensure_ascii = False, indent = 4)
	
	raw_inverted_dict = []
	indict_keys = list(indict.keys());
	
	for i in range(len(indict_keys)):
		raw_inverted_dict.append([indict[indict_keys[i]], indict_keys[i]])
	
	ENG_to_THA = {}
	
	for pair in raw_inverted_dict:
		if pair[0] in ENG_to_THA:
			ENG_to_THA[pair[0]].append(pair[1])
		else:
			ENG_to_THA[pair[0]] = []
			ENG_to_THA[pair[0]].append(pair[1])
	
	with open('ENG_to_THA.json','w',encoding='utf-8') as engtotha:
		json.dump(ENG_to_THA, engtotha, ensure_ascii = False, indent = 4)

# jsonize(Dictionarize())

app = Flask(__name__)

@app.route('/')
def Index():
	with open('ENG_to_THA.json','r',encoding='utf-8') as engtotha:
		Dict = json.load(engtotha)
	if request.args:
		req = request.args['wordform']
		try:
			translated = Dict[req]
			ids = [str(i+1) for i in range(len(translated))]
			result = [[ids[i], translated[i]] for i in range(len(translated))]
		except:
			result = [['Error', 'Something went wrong during the process.']]
		return render_template('index.html', result = result)
	return render_template('index.html', result = '')

if __name__ == '__main__':
	app.run(debug=True)