import re
import operator
import json
import urllib

from pymystem3 import Mystem
import pymorphy2

# from bs4 import BeautifulSoup

from flask import Flask
from flask import render_template
from flask import request

def getDict(filename):
	with open(filename,'r',encoding='utf-8') as injson:
		return json.load(injson)

strippedHTML = []
words = []
Words = []
outwords = []

m = Mystem()
pm = pymorphy2.MorphAnalyzer()
Dict = getDict('doref.json')

app = Flask(__name__)

class Word:
	def __init__(self, pos):
		self.wordform = words[pos]
		self.casetype = 'lower'
		self.lemma = ''
		self.output = self.wordform
		self.PoS = None # 'S', 'V', 'Adj', 'Adv', 'INTJ', 'PREP', 'CONJ', 'PRO'
		self.Gender = None # None, 'm', 'f', 'n'
		self.Number = None # None, 'sg', 'pl'
		self.Case = None # None, 'nom', 'gen', 'dat', 'acc', 'ins', 'abl'
		self.Power = None # None, 'comp', 'super'
		self.Tense = None # None, 'prs', 'pst, 'fut'
		self.stem = ''
		self.flex = ''
		self.prev = None
		self.next = None
		self.isSlike = False
		
		# retrieving case
		if self.wordform.islower(): self.casetype = 'lower'
		elif self.wordform[1:].islower(): self.casetype = 'title'
		elif self.wordform.isupper(): self.casetype = 'upper'
		
		# preparing for lemmatization
		self.wordform = self.wordform.lower()
		
		# setting self.prev
		if pos>0:
			self.prev = Words[pos-1]
		
		# setting self.lemma
		self.lemma = m.lemmatize(self.wordform)[0]
		
		# setting self.stem and self.flex
		Changed = False
		
		for i in range(len(self.wordform)):
			if i >= len(self.lemma):
				self.flex += self.wordform[i]
				continue
			if Changed:
				self.flex += self.wordform[i]
			else:
				if self.wordform[i] == self.lemma[i]:
					self.stem += self.wordform[i]
				else:
					Changed = True
					self.flex += self.wordform[i]
		
		try:
			rawstr = m.analyze(self.wordform)[0]['analysis'][0]['gr']
		except:
			self.PoS = 'S'
			return None
		
		# magically convert mystem string into json
		rawstr = re.sub(r'([a-zA-Zа-яёА-Яё0-9-]+)',r'"\g<1>"',rawstr)
		rawstr = re.sub(r'=\(',r':[{',rawstr)
		rawstr = re.sub('=',',',rawstr)
		rawstr = re.sub(r'\|',r'},{',rawstr)
		rawstr = re.sub(r'\)',r'}]',rawstr)
		rawstr = '{'+rawstr+'}'
		rawstr = re.sub(r',"',r':0,"',rawstr)
		rawstr = re.sub(r'"}',r'":0}',rawstr)
		rawstr = re.sub(r'}:0',r'}',rawstr)
		rawstr = re.sub(r',}',':0}',rawstr)
		
		Answer = json.loads(rawstr)
		k = set(Answer.keys())
		
		# setting self.PoS and self.isSlike
		if 'S' in k:
			self.PoS = 'S'
			self.isSlike = True
		elif 'V' in k:
			self.PoS = 'V'
		elif 'A' in k:
			self.PoS = 'Adj'
		elif 'ADV' in k:
			self.PoS = 'Adv'
		elif 'ADVPRO' in k:
			self.PoS = 'Pron-Adv'
		elif 'ANUM' in k:
			self.PoS = 'Pron-Num'
		elif 'APRO' in k:
			self.PoS = 'Pron-Adj'
		elif 'COM' in k:
			self.PoS = 'com'
		elif 'Conj' in k:
			self.PoS = 'Conj'
		elif 'INTJ' in k:
			self.PoS = 'Mejdom'
		elif 'Num' in k:
			self.PoS = 'Num'
		elif 'Part' in k:
			self.PoS = 'Part'
		elif 'PR' in k:
			self.PoS = 'Prep'
		elif 'SPRO' in k:
			self.PoS = 'Pron-S'
			self.isSlike = True
		
		if self.isSlike:
			# setting self.Gender
			if 'муж' in k:
				self.Gender = 'm'
			elif 'жен' in k:
				self.Gender = 'f'
			elif 'сред' in k:
				self.Gender = 'n'
			else:
				Break = False
				ana = pm.parse(self.wordform)
				for p in ana:
					if p.tag.POS == 'NOUN' or p.tag.POS == 'NPRO':
						if p.tag.gender:
							self.Gender = p.tag.gender[0]
							Break = True
							break
				if not Break: self.Gender = 'm'
			Break = False
			
			numberPossibilities = []
			# setting self.Number
			if 'неод' in k:
				try:
					Answer['неод'][0]
					for i in range(len(Answer['неод'])):
						numberPossibilities.append([])
						l = set(Answer['неод'][i].keys())
						if 'мн' in l:
							numberPossibilities[i].append('pl')
						elif 'ед' in l:
							numberPossibilities[i].append('sg')
				except:
					if 'мн' in k:
						self.Number = 'pl'
					elif 'ед' in k:
						self.Number = 'sg'
			elif 'од' in k:
				try:
					Answer['од'][0]
					for i in range(len(Answer['од'])):
						numberPossibilities.append([])
						l = set(Answer['од'][i].keys())
						if 'мн' in l:
							numberPossibilities[i].append('pl')
						elif 'ед' in l:
							numberPossibilities[i].append('sg')
				except:
					if 'мн' in k:
						self.Number = 'pl'
					elif 'ед' in k:
						self.Number = 'sg'
			
			# setting self.Case
			if 'неод' in k:
				try:
					Answer['неод'][0]
					for i in range(len(Answer['неод'])):
						if len(numberPossibilities[i])==0:
							numberPossibilities[i].append(self.Gender)
						l = set(Answer['неод'][i].keys())
						if 'им' in l:
							numberPossibilities[i].append('nom')
						elif 'род' in l:
							numberPossibilities[i].append('gen')
						elif 'дат' in l:
							numberPossibilities[i].append('dat')
						elif 'вин' in l:
							numberPossibilities[i].append('acc')
						elif 'твор' in l:
							numberPossibilities[i].append('ins')
						elif 'пр' in l:
							numberPossibilities[i].append('abl')
						elif 'парт' in l:
							numberPossibilities[i].append('part')
						elif 'местн' in l:
							numberPossibilities[i].append('loc')
						elif 'зват' in l:
							numberPossibilities[i].append('voc')
				except:
					if 'им' in k:
						self.Case = 'nom'
					elif 'род' in k:
						self.Case = 'gen'
					elif 'дат' in k:
						self.Case = 'dat'
					elif 'вин' in k:
						self.Case = 'acc'
					elif 'твор' in k:
						self.Case = 'ins'
					elif 'пр' in k:
						self.Case = 'abl'
					elif 'парт' in k:
						self.Case = 'part'
					elif 'местн' in k:
						self.Case = 'loc'
					elif 'зват' in k:
						self.Case = 'voc'
			elif 'од' in k:
				try:
					Answer['од'][0]
					for i in range(len(Answer['од'])):
						if len(numberPossibilities[i])==0:
							numberPossibilities[i].append(self.Gender)
						l = set(Answer['од'][i].keys())
						if 'им' in l:
							numberPossibilities[i].append('nom')
						elif 'род' in l:
							numberPossibilities[i].append('gen')
						elif 'дат' in l:
							numberPossibilities[i].append('dat')
						elif 'вин' in l:
							numberPossibilities[i].append('acc')
						elif 'твор' in l:
							numberPossibilities[i].append('ins')
						elif 'пр' in l:
							numberPossibilities[i].append('abl')
						elif 'парт' in l:
							numberPossibilities[i].append('part')
						elif 'местн' in l:
							numberPossibilities[i].append('loc')
						elif 'зват' in l:
							numberPossibilities[i].append('voc')
				except:
					if 'им' in k:
						self.Case = 'nom'
					elif 'род' in k:
						self.Case = 'gen'
					elif 'дат' in k:
						self.Case = 'dat'
					elif 'вин' in k:
						self.Case = 'acc'
					elif 'твор' in k:
						self.Case = 'ins'
					elif 'пр' in k:
						self.Case = 'abl'
					elif 'парт' in k:
						self.Case = 'part'
					elif 'местн' in k:
						self.Case = 'loc'
					elif 'зват' in k:
						self.Case = 'voc'
			
			# using pymorphy to resolve disambiguation
			if len(numberPossibilities)>0:
				ana = pm.parse(self.wordform)
				Break = False
				for p in ana:
					if p.tag.POS != 'NOUN' and p.tag.POS != 'NPRO': continue
					
					pm_number = p.tag.number
					if pm_number == 'sing': pm_number = 'sg'
					elif pm_number == 'plur': pm_number = 'pl'
					else: pm_number = None
					
					pm_case = p.tag.case
					if pm_case == 'nomn': pm_case = 'nom'
					elif pm_case == 'gent': pm_case = 'gen'
					elif pm_case == 'datv': pm_case = 'dat'
					elif pm_case == 'accs': pm_case = 'acc'
					elif pm_case == 'ablt': pm_case = 'ins'
					elif pm_case == 'loct': pm_case = 'abl'
					elif pm_case == 'voct': pm_case = 'voc'
					elif pm_case == 'gen2': pm_case = 'part'
					elif pm_case == 'acc2': pm_case = 'acc'
					elif pm_case == 'loc2': pm_case = 'loc'
					else: pm_case = None
					
					Break = False
					for possibility in numberPossibilities:
						if (pm_number in possibility) and (pm_case in possibility):
							Break = True
							self.Number = pm_number
							self.Case = pm_case
							break
					if Break: break
				if not Break:
					self.Number = numberPossibilities[0][0]
					self.Case = numberPossibilities[0][1]
				Break = False
		
		
		elif self.PoS == 'Adj':
			numberPossibilities = []
			try:
				Answer['A'][0]
				for i in range(len(Answer['A'])):
					k = set(Answer['A'][i].keys())
					
					numberPossibilities.append([])
					# setting Gender
					if 'муж' in k:
						numberPossibilities[i].append('m')
					elif 'жен' in k:
						numberPossibilities[i].append('f')
					elif 'сред' in k:
						numberPossibilities[i].append('n')
					elif 'мж' in k:
						Break = False
						ana = pm.parse(self.wordform)
						for p in ana:
							if p.tag.POS == 'NOUN' or p.tag.POS == 'NPRO':
								if p.tag.gender:
									self.Gender = p.tag.gender[0]
									Break = True
									break
						if not Break: numberPossibilities[i].append('m')
					Break = False
					
					# setting Number
					if 'мн' in k:
						numberPossibilities[i].append('pl')
					elif 'ед' in k:
						numberPossibilities[i].append('sg')
					
					# setting Case
					if 'им' in k:
						numberPossibilities[i].append('nom')
					elif 'род' in k:
						numberPossibilities[i].append('gen')
					elif 'дат' in k:
						numberPossibilities[i].append('dat')
					elif 'вин' in k:
						numberPossibilities[i].append('acc')
					elif 'твор' in k:
						numberPossibilities[i].append('ins')
					elif 'пр' in k:
						numberPossibilities[i].append('abl')
					elif 'парт' in k:
						numberPossibilities[i].append('part')
					elif 'местн' in k:
						numberPossibilities[i].append('loc')
					elif 'зват' in k:
						numberPossibilities[i].append('voc')
					
					# setting self.Power
					if 'срав' in k:
						numberPossibilities[i].append('comp')
					elif 'прев' in k:
						numberPossibilities[i].append('super')
					else:
						numberPossibilities[i].append(None)
			except:
				# setting self.Gender
				if 'муж' in k:
					self.Gender = 'm'
				elif 'жен' in k:
					self.Gender = 'f'
				elif 'сред' in k:
					self.Gender = 'n'
				else:
					Break = False
					ana = pm.parse(self.wordform)
					for p in ana:
						if p.tag.POS == 'NOUN' or p.tag.POS == 'NPRO':
							if p.tag.gender:
								self.Gender = p.tag.gender[0]
								Break = True
								break
					if not Break: self.Gender = 'm'
				Break = False
				
				# setting self.Number
				if 'мн' in k:
					self.Number = 'pl'
				elif 'ед' in k:
					self.Number = 'sg'
				
				# setting self.Case
				if 'им' in k:
					self.Case = 'nom'
				elif 'род' in k:
					self.Case = 'gen'
				elif 'дат' in k:
					self.Case = 'dat'
				elif 'вин' in k:
					self.Case = 'acc'
				elif 'твор' in k:
					self.Case = 'ins'
				elif 'пр' in k:
					self.Case = 'abl'
				elif 'парт' in k:
					self.Case = 'part'
				elif 'местн' in k:
					self.Case = 'loc'
				elif 'зват' in k:
					self.Case = 'voc'
				
				# setting self.Power
				if 'срав' in k:
					self.Power = 'comp'
				elif 'прев' in k:
					self.Power = 'super'
			
			# using pymorphy to resolve disambiguation
			if len(numberPossibilities)>0:
				ana = pm.parse(self.wordform)
				Break = False
				for p in ana:
					if p.tag.POS != 'ADJF' and p.tag.POS != 'ADJS': continue
					if p.tag.gender: pm_gender = p.tag.gender[0]
					else: pm_gender = None
					
					pm_number = p.tag.number
					if pm_number == 'sing': pm_number = 'sg'
					elif pm_number == 'plur': pm_number = 'pl'
					else: pm_number = None
					
					pm_case = p.tag.case
					if pm_case == 'nomn': pm_case = 'nom'
					elif pm_case == 'gent': pm_case = 'gen'
					elif pm_case == 'datv': pm_case = 'dat'
					elif pm_case == 'accs': pm_case = 'acc'
					elif pm_case == 'ablt': pm_case = 'ins'
					elif pm_case == 'loct': pm_case = 'abl'
					elif pm_case == 'voct': pm_case = 'voc'
					elif pm_case == 'gen2': pm_case = 'part'
					elif pm_case == 'acc2': pm_case = 'acc'
					elif pm_case == 'loc2': pm_case = 'loc'
					else: pm_case = None
					
					Break = False
					for possibility in numberPossibilities:
						if (pm_number in possibility) and (pm_case in possibility):
							Break = True
							self.Number = pm_number
							self.Case = pm_case
							self.Power = possibility[-1]
							break
					if Break: break
				if not Break:
					self.Number = numberPossibilities[0][0]
					self.Case = numberPossibilities[0][1]
				Break = False
	
	def setNext(self,pos):
		if pos<len(Words)-1:
			self.next = Words[pos+1]
	
	def Transform(self):
		# General
		# setting letters ѣ, ѳ, ѵ
		if self.lemma in set(Dict.keys()):
			x = len(self.stem)
			self.stem = Dict[self.lemma][:x]
	#	print(self.lemma,self.stem,self.flex)
		# dealing with без-, через-, чрез-
		if self.stem[:3] == 'бес': self.stem = 'бес'+self.stem[3:]
		if self.stem[:4] == 'чрес': self.stem = 'чрес'+self.stem[4:]
		if self.stem[:5] == 'черес': self.stem = 'черес'+self.stem[5:]
		
		# Noun-like
		if self.isSlike or self.PoS == 'A':
			# dealing with ѣ in dat, abl & loc
			if (self.Case == 'dat' or self.Case == 'abl' or self.Case == 'loc') and (re.search('е',self.flex)): self.flex = re.sub('е','ѣ',self.flex)
			elif (self.Case == 'dat' or self.Case == 'abl' or self.Case == 'loc') and self.stem[-1] == 'е' and (self.wordform == self.stem):
				self.stem = self.stem[:-1]
				self.flex = 'ѣ'

		# Adjective
		if self.PoS == 'A':
			# dealing with ѣ in comparative and superlative
			if (self.Power == 'super' or self.Power == 'comp') and re.search('е',self.flex) and not (self.flex == 'е'):
				self.flex = re.sub('e','ѣ',self.flex)
				self.flex = re.sub('ѣѣ','ѣе',self.flex)
		
		# Merging stem and flex
		self.output = self.stem + self.flex
		
		# Adjective again
		if self.PoS == 'A':
			# dealing with -ія, -ыя, -іяся
			if self.Gender != 'm' and (((self.prev.Gender == 'f' or self.prev.Gender == 'n') and self.prev.isSlike and self.prev.Gender == self.Gender and self.prev.Number == self.Number and self.prev.Case == self.Case) or ((self.next.Gender == 'f' or self.next.Gender == 'n') and self.next.isSlike and self.next.Gender == self.Gender and self.next.Number == self.Number and self.next.Case == self.Case)):
				if self.output[-2:] == 'ие':
					self.output = self.output[:-2]+'ия'
				elif self.output[-2:] == 'ые':
					self.output = self.output[:-2]+'ыя'
				elif self.output[-4:] == 'иеся':
					self.output = self.output[:-4]+'ияся'
		'''
		# Verb
		if self.PoS == 'V':
			# dealing with -ел, -ела, -ело, -ели, -еет, -евши, -евать
			if self.lemma[-3:] == 'еть' and not(self.lemma[-6:] == 'мереть' or self.lemma[-6:] == 'переть' or self.lemma[-6:] == 'тереть'):
				Base = self.output[len(self.lemma[:3]):]
				Flex = self.output[:len(self.lemma[:3])-len(self.output)]
				Flex = re.sub('e','ѣ',Flex)
				Flex = re.sub('ѣѣ','ѣе',Flex)
				self.output = Base+Flex
		'''
		
		
		# General
		# setting letter i
		self.output = re.sub(r'и([аеёиоуэюяѣѵ])',r'i\g<1>',self.output)
		# setting letter ъ
		if re.search(r'[бвгджзклмнпрстфхцчшщ]',self.output[-1]): self.output += 'ъ'
		# dealing with онѣ
		if self.wordform == 'они': self.output = 'онѣ'
		
		# little hotfix
		if self.output == 'чтó': self.output = 'что'
		
		# Reverting to original casetype
		if self.casetype == 'lower': self.output = self.output.lower()
		elif self.casetype == 'title': self.output = self.output.title()
		elif self.casetype == 'upper': self.output = self.output.upper()
		return self.output

@app.route('/')
def Index():
	skopje = ''
	if request.args:
		strippedHTML = [request.args['wordform']]
		translated = Word(0).Transform()
		return render_template('index.html', skopje = skopje, translated = translated)
	return render_template('index.html', skopje = skopje, translated = '')

@app.route('/webpage')
def TransliterateWebpage():
	Webpage = 'https://tjournal.ru/'
	html = urllib.request.urlopen(Webpage)
	strippedHTML = re.split(r'([а-яёА-ЯЁ]+)',html.read().decode('utf-8'))
	for piece in strippedHTML:
		if re.search(r'[а-яёА-ЯЁ]', piece):
			words.append(piece)
	for i in range(len(words)):
		Words.append(Word(i))
	for i in range(len(Words)):
		Words[i].setNext(i)
	for W in Words:
		outwords.append(W.Transform())
	outstr = ''
	k=0
	for piece in strippedHTML:
		if re.search(r'[а-яёА-ЯЁ]', piece):
			outstr += outwords[k]
			k+=1
		else:
			outstr += piece
	loop_here = """Самые частотные леммы:<br>
	{% for k, v in mostfrequent %}
        <li>{{ k }} - {{ v }}</li>
    {% endfor %}"""
	outstr = re.sub('<div class="live__content"></div>',loop_here,outstr)
	with open('templates/out.html','w',encoding='utf-8') as o:
		o.write(outstr)
	FreqDict = {}
	for W in Words:
		L = W.lemma
		if W.lemma in FreqDict:
			FreqDict[W.lemma] += 1
		else:
			FreqDict[W.lemma] = 1
	FreqList = [(k, FreqDict[k]) for k in sorted(FreqDict, key=FreqDict.get, reverse=True)]
	
	return render_template("out.html", mostfrequent = FreqList[:10])

if __name__ == '__main__':
	app.run(debug=True)
