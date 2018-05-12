import json
import requests
import re
import pymorphy2
from random import randint

from bs4 import BeautifulSoup

pm = pymorphy2.MorphAnalyzer()

def Base(word):
	parsed = pm.parse(word)[0]
	word_base = parsed.normal_form
	return word_base

def grammar_matches(word_orig,word_src):
	word_orig = Base(word_orig)
	word_src = Base(word_src)
	for i in pm.parse(word_orig):
		for k in pm.parse(word_src):
			i_tag = str(i.tag)
			k_tag = str(k.tag)
			i_tag = re.sub(r',[A-Z][a-z]+','',i_tag)
			k_tag = re.sub(r',[A-Z][a-z]+','',k_tag)
			if i_tag == k_tag:
				return k
	return None

def rusvectores_get(keyword,word):
	similarities_list = None
	Webpage = 'http://rusvectores.org/'+keyword+'/'+word.lower()+'/api/json'
	# print(Webpage)
	try:
		raw_json = requests.get(Webpage).text
		araneum_dict = json.loads(raw_json)
		similarities_list = list(araneum_dict[keyword][list(araneum_dict[keyword].keys())[0]].keys())
	except Exception as e:
		# print('Exception caught: '+str(e))
		pass
	return similarities_list

def similar_araneum(word):
	araneum_10similarities_list = rusvectores_get('araneum_none_fasttextcbow_300_5_2018',word)
	return araneum_10similarities_list

def similar_news(word):
	temp_list = rusvectores_get('news_upos_cbow_600_2_2018',word)
	if temp_list is None:
		return temp_list
	news_10similarities_list = []
	for item in temp_list:
		item = re.sub(r'_.*','',item)
		item = re.sub(r'(.*?)::.*','\1',item)
		news_10similarities_list.append(item)
	return news_10similarities_list

def similar_ruscorpora_wiki10(word):
	temp_list = rusvectores_get('ruwikiruscorpora_upos_skipgram_300_2_2018',word)
	if temp_list is None:
		return temp_list
	ruscorpora_wiki_10similarities_list = []
	for item in temp_list:
		ruscorpora_wiki_10similarities_list.append(re.sub(r'_.*','',item))
	return ruscorpora_wiki_10similarities_list

def similar_ruscorpora(word):
	temp_list = rusvectores_get('ruscorpora_upos_skipgram_300_5_2018',word)
	if temp_list is None:
		return temp_list
	ruscorpora_10similarities_list = []
	for item in temp_list:
		ruscorpora_10similarities_list.append(re.sub(r'_.*','',item))
	return ruscorpora_10similarities_list

def synonims(word):
	synonims_dictionary_list_for_word = None
	Webpage = 'http://synonymonline.ru/'+word[0].upper()+'/'+word.lower()
	# print(Webpage)
	try:
		html = requests.get(Webpage).text
		if re.search("имеет следующие синонимы:",html):
			# print("HTML for roots retrieved")
			soup = BeautifulSoup(html, 'html.parser')
			pretext = soup.find("p", string=re.compile("имеет следующие синонимы:"))
			descendant_string = pretext.next_sibling.next_sibling.get_text()
			descendants_list = descendant_string.split('\n')
	except Exception as e:
		# print('Exception caught: '+str(e))
		pass
	return synonims_dictionary_list_for_word

def makedict():
	with open ('./Dictionary.txt', 'r', encoding='utf-8') as D:
		Dictionary = D.readlines()
	return Dictionary

def is_descendant(possibleChild,possibleParent):
	BoolForDescenancyIfSameRoot = False
	Webpage = 'http://wordroot.ru/'+possibleParent.lower()
	try:
		html = requests.get(Webpage).text
		if re.search("имеет следующие однокоренные слова:",html):
		#	# print("HTML for roots retrieved")
			soup = BeautifulSoup(html, 'html.parser')
			pretext = soup.find("p", string=re.compile("имеет следующие однокоренные слова:"))
			descendant_string = pretext.next_sibling.next_sibling.get_text()
			descendants_list = descendant_string.split('\n')
			if possibleChild.lower() in descendants_list:
				BoolForDescenancyIfSameRoot = True
	except Exception as e:
		# print('Exception caught: '+str(e))
		pass

	# TRY Sideways:

	Webpage = 'http://wordroot.ru/'+possibleChild.lower()
	try:
		html = requests.get(Webpage).text
		if re.search("имеет следующие однокоренные слова:",html):
		#	# print("Reversed HTML for roots retrieved")
			soup = BeautifulSoup(html, 'html.parser')
			pretext = soup.find("p", string=re.compile("имеет следующие однокоренные слова:"))
			descendant_string = pretext.next_sibling.next_sibling.get_text()
			descendants_list = descendant_string.split('\n')
			if possibleParent.lower() in descendants_list:
				BoolForDescenancyIfSameRoot = True
	except Exception as e:
		# print('Exception caught: '+str(e))
		pass

	return BoolForDescenancyIfSameRoot

def get_similar_word(word):
	cases = [letter.isupper() for letter in word]
	similar = ""
	response = ""
	parsed = pm.parse(word)[0]
	base = Base(word)
	araneum10 = similar_araneum(base)
	v_status = '<~'
	if araneum10 is not None:
		for entity in araneum10:
			if re.search(r'[^\w-]',entity):
				continue
			agreement = grammar_matches(base,entity)
			if agreement is not None and not is_descendant(entity,base):
				if len(str(parsed.tag).split(' ')) > 1:
					inflected = agreement.inflect(frozenset(str(parsed.tag).split(' ')[1].split(',')))
					if inflected is not None:
						response = inflected.word
						stat_reason = 'via araneum_none_fasttextcbow_300_5_2018'
					else:
						continue
				else:
					response = agreement.word
					stat_reason = 'via araneum_none_fasttextcbow_300_5_2018'
				break
	if response == "":
		news10 = similar_news(base)
		if news10 is not None:
			for entity in news10:
				if re.search(r'[^\w-]',entity):
					continue
				agreement = grammar_matches(base,entity)
				if agreement is not None and not is_descendant(entity,base):
					if len(str(parsed.tag).split(' ')) > 1:
						inflected = agreement.inflect(frozenset(str(parsed.tag).split(' ')[1].split(',')))
						if inflected is not None:
							response = inflected.word
							stat_reason = 'via news_upos_cbow_600_2_2018'
						else:
							continue
					else:
						response = agreement.word
						stat_reason = 'via news_upos_cbow_600_2_2018'
					break
		if response == "":
			ruscorpora_wiki10 = similar_ruscorpora_wiki10(base)
			if ruscorpora_wiki10 is not None:
				for entity in ruscorpora_wiki10:
					if re.search(r'[^\w-]',entity):
						continue
					agreement = grammar_matches(base,entity)
					if agreement is not None and not is_descendant(entity,base):
						if len(str(parsed.tag).split(' ')) > 1:
							inflected = agreement.inflect(frozenset(str(parsed.tag).split(' ')[1].split(',')))
							if inflected is not None:
								response = inflected.word
								stat_reason = 'via ruwikiruscorpora_upos_skipgram_300_2_2018'
							else:
								continue
						else:
							response = agreement.word
							stat_reason = 'via ruwikiruscorpora_upos_skipgram_300_2_2018'
						break
			if response == "":
				ruscorpora10 = similar_ruscorpora(base)
				if ruscorpora10 is not None:
					for entity in ruscorpora10:
						if re.search(r'[^\w-]',entity):
							continue
						agreement = grammar_matches(base,entity)
						if agreement is not None and not is_descendant(entity,base):
							if len(str(parsed.tag).split(' ')) > 1:
								inflected = agreement.inflect(frozenset(str(parsed.tag).split(' ')[1].split(',')))
								if inflected is not None:
									response = inflected.word
									stat_reason = 'via ruscorpora_upos_skipgram_300_5_2018'
								else:
									continue
							else:
								response = agreement.word
								stat_reason = 'via ruscorpora_upos_skipgram_300_5_2018'
							break
				if response == "":
					synonymsdict = synonims(base)
					if synonymsdict is not None:
						for entity in synonymsdict:
							if re.search(r'[^\w-]',entity):
								continue
							agreement = grammar_matches(base,entity)
							if agreement is not None and not is_descendant(entity,base):
								if len(str(parsed.tag).split(' ')) > 1:
									inflected = agreement.inflect(frozenset(str(parsed.tag).split(' ')[1].split(',')))
									if inflected is not None:
										response = inflected.word
										stat_reason = 'via synonymonline.ru'
									else:
										continue
								else:
									response = agreement.word
									stat_reason = 'via synonymonline.ru'
								break
					if response == "":
						i = 0
						Dictionary = makedict()
						while i<200:
							used_ids = []
							next_id = randint(0,len(Dictionary)-1)
							while next_id in used_ids:
								next_id = randint(0,len(Dictionary)-1)
							entity = re.sub(r'\W','',Dictionary[next_id])
							if re.search(r'[^\w-]',entity):
								continue
							# print(entity)
							agreement = grammar_matches(base,entity)
							if agreement is not None and not is_descendant(entity,base):
								if len(str(parsed.tag).split(' ')) > 1:
									inflected = agreement.inflect(frozenset(str(parsed.tag).split(' ')[1].split(',')))
									if inflected is not None:
										response = inflected.word
										stat_reason = 'via Tikhonov-based dictionary search'
									else:
										continue
								else:
									response = agreement.word
									stat_reason = 'via Tikhonov-based dictionary search'
								break
							used_ids.append(next_id)
							i+=1
						if response == "":
							response = word
							v_status = '=='
							stat_reason = 'due to Not Found'

	'''
	print(response)
	if agreement is not None:
		if agreement.tag is not None:
			print(agreement.tag)
	'''

	if len(cases)<len(response):
		C = True
		for el in cases:
			if not el: C = False
		if C: cases = [True for letter in response]
		else:
			C = True
			for el in cases:
				if el: C = False
			if C: cases = [False for letter in response]
			else:
				C = cases[0]
				for i in range(len(cases)-1):
					if cases[i+1] == C:
						C = ""
						break
					else:
						C = not C
				if isinstance(C, bool):
					new_cases = []
					C = cases[0]
					for letter in response:
						new_cases.append(C)
						C = not C
					cases = new_cases
				else:
					for i in range(len(cases)-1):
						if (cases[i] != cases[i+1]):
							new_cases = [cases[i] for k in range(i+1)]
							for k in range(len(response)-i-1):
								new_cases.append(not cases[i])
							cases = new_cases
							break
		if len(cases) != len(response):
			cases = [False for letter in response]

	for i in range(len(response)):
		if cases[i]:
			similar += response[i].upper()
		else:
			similar += response[i].lower()

	print(word+' '+v_status+' '+similar+' '+stat_reason)
	return similar

def get_similar_text(textstring):
	allow_PoS = ('NOUN', 'ADJF', 'ADJS', 'COMP', 'VERB', 'INFN', 'PRTF', 'PRTS', 'GRND', 'ADVB', 'PRED')
	words_mess = re.split(r'([^\w-])',textstring)
	similar_string = ""
	print()
	print('NEW REQUEST: "'+textstring+'"')
	for i in range(len(words_mess)):
		if re.search(r'\w',words_mess[i]):
			parsed = pm.parse(words_mess[i].lower())[0]
			if parsed.tag.POS in allow_PoS and not re.search('Apro|Anum',str(parsed.tag)):
				similar_string += get_similar_word(words_mess[i])
			else:
				similar_string += words_mess[i]
				print(words_mess[i]+' == '+words_mess[i]+' due to ('+str(parsed.tag)+')')
		else:
			similar_string += words_mess[i]
	return similar_string