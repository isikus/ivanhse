import json
import urllib.request
import re
from os import listdir, makedirs, chdir, sep, path, remove
from random import shuffle

# Здесь начинается часть для домашки
import sqlite3
from sqlite3 import Error

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

import datetime
from dateutil.relativedelta import relativedelta
# Здесь заканчивается часть для домашки

def create_connection(db_file):
	""" create a database connection to a SQLite database """
	try:
		conn = sqlite3.connect(db_file)
	except Error as e:
		print(e)
	finally:
		conn.close()

def CountLength(textstring):
	wtokens = textstring.split()
	length = 0
	for w in wtokens:
		if re.search(r'\W',w): length += 1
	return length

def get_posts():
	print('Как удачно, что мне уже пришлось писать код для выкачки из вк для проекта по социолингвистике, и для этой домашки осталось лишь немного его адаптировать. Поэтому прошу прощения, если из-за этого он окажется немного неформатным, - зато можно посмотреть на результат нашего проекта: https://tinyurl.com/lexicalportrait')
	token = input('Введите действительный ключ доступа: ')
	public_id = input('Введите id паблика (например, -57354358): ')
	offset = int(input('Введите, сколько постов назад была самая старая интересущая вас запись (например, 250): '))
	count_total = int(input('Введите, какое количество постов нужно обработать (например, 150): '))
	rand_choice = count_total
	include_comments = True
	if input('Введите "да", если нужно очищать текст от ссылок на страницы вк: ') == 'да':
		clean_links = True
	else:
		clean_links = False
	if input('Введите "verbose" для более подробной выдачи программы: ') == 'verbose':
		verbose = True
	else:
		verbose = False
	
	Total = 0
	fTotal = count_total
	
	Dict = {}
	
	makedirs("./"+public_id, exist_ok=True)
	chdir(public_id)
	
	# Здесь начинается часть для домашки
	conn = sqlite3.connect('db.sqlite')
	cur = conn.cursor()
	cur.execute("CREATE TABLE public%s (id INTEGER, Post TEXT, PostLength INTEGER, MeanCommentsLength REAL)" % public_id[1:])
	cur.execute("CREATE TABLE Comments (Comment TEXT, CommentLength INTEGER, Author_id INTEGER, AuthorAge INTEGER, AuthorCity TEXT, AuthorCity_id INTEGER)")
	# cur.execute("CREATE TABLE Posts (Post TEXT, PostLength INTEGER, Author_id INTEGER, AuthorAge INTEGER, AuthorCity TEXT, AuthorCity_id INTEGER)")
	conn.commit()
	# Здесь заканчивается часть для домашки
	
	while (count_total // 100):
		Succeed = False
		while (not Succeed):
			response = urllib.request.urlopen("https://api.vk.com/method/wall.get?owner_id=%s&offset=%s&count=%s&access_token=%s&v=5.69" % (public_id, str(offset), '100', token))
			if verbose:
				print("Loaded https://api.vk.com/method/wall.get?owner_id=%s&offset=%s&count=%s&access_token=%s&v=5.69" % (public_id, str(offset), '100', token))
			json_string = response.read().decode('utf-8')
			current_request = json.loads(json_string)
			try:
				current_request['response']
				Succeed = True
			except:
				print('Failed to get request, resending')
				Succeed = False
		for item in current_request['response']['items']:
			try:
				text = item['text']
				Dict[str(item['id'])]={}
				if clean_links:
					text = re.sub(r'\[.*?\|(.*?)\]','\g<1>',text)
				text = re.sub(r'\<.*?\>',' ',text)
				Dict[str(item['id'])]['Text']=text
				Total += 1
				if verbose:
					print("Processing item %s with id %s. %s to go" % (str(Total), str(item['id']), str(fTotal-Total)))
				if include_comments:
					current_post_comments = []
					comments_count = item['comments']['count']
					while (comments_count // 100):
						Succeed = False
						while (not Succeed):
							response = urllib.request.urlopen("https://api.vk.com/method/wall.getComments?owner_id=%s&post_id=%s&count=100&preview_length=0&access_token=%s&v=5.69" % (public_id, str(item['id']), token))
							json_string = response.read().decode('utf-8')
							current_request = json.loads(json_string)
							try:
								current_request['response']
								Succeed = True
							except:
								print('Failed to get request for COMMENTS, resending')
								Succeed = False
						for comment in current_request['response']['items']:
							try:
								text = comment['text']
								if clean_links:
									text = re.sub(r'\[.*?\|(.*?)\]','\g<1>',text)
								text = re.sub(r'\<.*?\>',' ',text)
								current_post_comments.append(text)
								# Здесь начинается часть для домашки
								userid = str(comment['id'])
								if userid[0] != '-':
									Succeed = False
									while (not Succeed):
										response = urllib.request.urlopen("https://api.vk.com/method/users.get?user_ids=%s&fields=bdate,city&name_case=Nom&access_token=%s&v=5.69" % (userid, token))
										json_string = response.read().decode('utf-8')
										current_request = json.loads(json_string)
										try:
											current_request['response'][0]
											Succeed = True
										except:
											print('Failed to get request for User, resending')
											Succeed = False
									user = current_request['response'][0]
									if "city" in user:
										user_city_id = user["city"]["id"]
										user_city_name = user["city"]["title"]
										if "bday" in user:
											if len(user["bday"])>=8:
												bday = datetime.datetime.strptime(user["bdate"],"%d.%m.%Y")
												now = datetime.datetime.now()
												user_age = relativedelta(now, bday).years
												cur.execute("INSERT INTO Comments (Comment, CommentLength, Author_id, AuthorAge, AuthorCity, AuthorCity_id) VALUES (?, ?, ?, ?, ?, ?)", [text, CountLength(text), int(userid), user_age, user_city_name, user_city_id])
												conn.commit()
											else:
												cur.execute("INSERT INTO Comments (Comment, CommentLength, Author_id, AuthorCity, AuthorCity_id) VALUES (?, ?, ?, ?, ?)", [text, CountLength(text), int(userid), user_city_name, user_city_id])
												conn.commit()
										else:
											cur.execute("INSERT INTO Comments (Comment, CommentLength, Author_id, AuthorCity, AuthorCity_id) VALUES (?, ?, ?, ?, ?)", [text, CountLength(text), int(userid), user_city_name, user_city_id])
											conn.commit()
									else:
										if "bday" in user:
											if len(user["bday"])>=8:
												bday = datetime.datetime.strptime(user["bdate"],"%d.%m.%Y")
												now = datetime.datetime.now()
												user_age = relativedelta(now, bday).years
												cur.execute("INSERT INTO Comments (Comment, CommentLength, Author_id, AuthorAge) VALUES (?, ?, ?, ?)", [text, CountLength(text), int(userid), user_age])
												conn.commit()
								# Здесь заканчивается часть для домашки
							except:
								print('Exception caught while processing comments')
						comments_count -= 100
					Succeed = False
					while (not Succeed):
						response = urllib.request.urlopen("https://api.vk.com/method/wall.getComments?owner_id=%s&post_id=%s&count=100&preview_length=0&access_token=%s&v=5.69" % (public_id, str(item['id']), token))
						json_string = response.read().decode('utf-8')
						current_request = json.loads(json_string)
						try:
							current_request['response']
							Succeed = True
						except:
							print('Failed to get request for COMMENTS, resending')
							Succeed = False
					for comment in current_request['response']['items']:
						try:
							text = comment['text']
							if clean_links:
								text = re.sub(r'\[.*?\|(.*?)\]','\g<1>',text)
							text = re.sub(r'\<.*?\>',' ',text)
							current_post_comments.append(text)
							# Здесь начинается часть для домашки
							userid = str(comment['id'])
							if userid[0] != '-':
								Succeed = False
								while (not Succeed):
									response = urllib.request.urlopen("https://api.vk.com/method/users.get?user_ids=%s&fields=bdate,city&name_case=Nom&access_token=%s&v=5.69" % (userid, token))
									json_string = response.read().decode('utf-8')
									current_request = json.loads(json_string)
									try:
										current_request['response'][0]
										Succeed = True
									except:
										print('Failed to get request for User, resending')
										Succeed = False
								user = current_request['response'][0]
								if "city" in user:
									user_city_id = user["city"]["id"]
									user_city_name = user["city"]["title"]
									if "bday" in user:
										if len(user["bday"])>=8:
											bday = datetime.datetime.strptime(user["bdate"],"%d.%m.%Y")
											now = datetime.datetime.now()
											user_age = relativedelta(now, bday).years
											cur.execute("INSERT INTO Comments (Comment, CommentLength, Author_id, AuthorAge, AuthorCity, AuthorCity_id) VALUES (?, ?, ?, ?, ?, ?)", [text, CountLength(text), int(userid), user_age, user_city_name, user_city_id])
											conn.commit()
										else:
											cur.execute("INSERT INTO Comments (Comment, CommentLength, Author_id, AuthorCity, AuthorCity_id) VALUES (?, ?, ?, ?, ?)", [text, CountLength(text), int(userid), user_city_name, user_city_id])
											conn.commit()
									else:
										cur.execute("INSERT INTO Comments (Comment, CommentLength, Author_id, AuthorCity, AuthorCity_id) VALUES (?, ?, ?, ?, ?)", [text, CountLength(text), int(userid), user_city_name, user_city_id])
										conn.commit()
								else:
									if "bday" in user:
										if len(user["bday"])>=8:
											bday = datetime.datetime.strptime(user["bdate"],"%d.%m.%Y")
											now = datetime.datetime.now()
											user_age = relativedelta(now, bday).years
											cur.execute("INSERT INTO Comments (Comment, CommentLength, Author_id, AuthorAge) VALUES (?, ?, ?, ?)", [text, CountLength(text), int(userid), user_age])
											conn.commit()
							# Здесь заканчивается часть для домашки
						except:
							print('Exception caught while processing comments')
					Dict[str(item['id'])]['Comments']=current_post_comments
					# Здесь начинается часть для домашки
					cpcl = [CountLength(cmnt) for cmnt in current_post_comments]
					if len(current_post_comments) == 0:
						current_post_mean_comments_length = 0.0
					else:
						current_post_mean_comments_length = float(sum(cpcl)/len(current_post_comments))
					cur.execute("INSERT INTO public%s (id, Post, PostLength, MeanCommentsLength) VALUES (?, ?, ?, ?)" % public_id[1:], [item["id"], Dict[str(item['id'])]['Text'], CountLength(Dict[str(item['id'])]['Text']), current_post_mean_comments_length])
					conn.commit()
					# Здесь заканчивается часть для домашки
			except Exception as e:
				print(str(e)+' happened while processing posts')
		offset -= 100
		count_total -= 100
	Succeed = False
	while (not Succeed):
		response = urllib.request.urlopen("https://api.vk.com/method/wall.get?owner_id=%s&offset=%s&count=%s&access_token=%s&v=5.69" % (public_id, str(offset), str(count_total), token))
		if verbose:
			print("Loaded https://api.vk.com/method/wall.get?owner_id=%s&offset=%s&count=%s&access_token=%s&v=5.69" % (public_id, str(offset), str(count_total), token))
		json_string = response.read().decode('utf-8')
		current_request = json.loads(json_string)
		try:
			current_request['response']
			Succeed = True
		except:
			print('Failed to get request, resending')
			Succeed = False
	for item in current_request['response']['items']:
		try:
			text = item['text']
			Dict[str(item['id'])]={}
			if clean_links:
				text = re.sub(r'\[.*?\|(.*?)\]','\g<1>',text)
			text = re.sub(r'\<.*?\>',' ',text)
			Dict[str(item['id'])]['Text']=text
			Total += 1
			if verbose:
				print("Processing item %s with id %s. %s to go" % (str(Total), str(item['id']), str(fTotal-Total)))
			if include_comments:
				current_post_comments = []
				comments_count = item['comments']['count']
				while (comments_count // 100):
					Succeed = False
					while (not Succeed):
						response = urllib.request.urlopen("https://api.vk.com/method/wall.getComments?owner_id=%s&post_id=%s&count=100&preview_length=0&access_token=%s&v=5.69" % (public_id, str(item['id']), token))
						json_string = response.read().decode('utf-8')
						current_request = json.loads(json_string)
						try:
							current_request['response']
							Succeed = True
						except:
							print('Failed to get request for COMMENTS, resending')
							Succeed = False
					for comment in current_request['response']['items']:
						try:
							text = comment['text']
							if clean_links:
								text = re.sub(r'\[.*?\|(.*?)\]','\g<1>',text)
							text = re.sub(r'\<.*?\>',' ',text)
							current_post_comments.append(text)
							# Здесь начинается часть для домашки
							userid = str(comment['id'])
							if userid[0] != '-':
								Succeed = False
								while (not Succeed):
									response = urllib.request.urlopen("https://api.vk.com/method/users.get?user_ids=%s&fields=bdate,city&name_case=Nom&access_token=%s&v=5.69" % (userid, token))
									json_string = response.read().decode('utf-8')
									current_request = json.loads(json_string)
									try:
										current_request['response'][0]
										Succeed = True
									except:
										print('Failed to get request for User, resending')
										Succeed = False
								user = current_request['response'][0]
								if "city" in user:
									user_city_id = user["city"]["id"]
									user_city_name = user["city"]["title"]
									if "bday" in user:
										if len(user["bday"])>=8:
											bday = datetime.datetime.strptime(user["bdate"],"%d.%m.%Y")
											now = datetime.datetime.now()
											user_age = relativedelta(now, bday).years
											cur.execute("INSERT INTO Comments (Comment, CommentLength, Author_id, AuthorAge, AuthorCity, AuthorCity_id) VALUES (?, ?, ?, ?, ?, ?)", [text, CountLength(text), int(userid), user_age, user_city_name, user_city_id])
											conn.commit()
										else:
											cur.execute("INSERT INTO Comments (Comment, CommentLength, Author_id, AuthorCity, AuthorCity_id) VALUES (?, ?, ?, ?, ?)", [text, CountLength(text), int(userid), user_city_name, user_city_id])
											conn.commit()
									else:
										cur.execute("INSERT INTO Comments (Comment, CommentLength, Author_id, AuthorCity, AuthorCity_id) VALUES (?, ?, ?, ?, ?)", [text, CountLength(text), int(userid), user_city_name, user_city_id])
										conn.commit()
								else:
									if "bday" in user:
										if len(user["bday"])>=8:
											bday = datetime.datetime.strptime(user["bdate"],"%d.%m.%Y")
											now = datetime.datetime.now()
											user_age = relativedelta(now, bday).years
											cur.execute("INSERT INTO Comments (Comment, CommentLength, Author_id, AuthorAge) VALUES (?, ?, ?, ?)", [text, CountLength(text), int(userid), user_age])
											conn.commit()
							# Здесь заканчивается часть для домашки
						except:
							print('Exception caught while processing comments')
					comments_count -= 100
				Succeed = False
				while (not Succeed):
					response = urllib.request.urlopen("https://api.vk.com/method/wall.getComments?owner_id=%s&post_id=%s&count=100&preview_length=0&access_token=%s&v=5.69" % (public_id, str(item['id']), token))
					json_string = response.read().decode('utf-8')
					current_request = json.loads(json_string)
					try:
						current_request['response']
						Succeed = True
					except:
						print('Failed to get request for COMMENTS, resending')
						Succeed = False
				for comment in current_request['response']['items']:
					try:
						text = comment['text']
						if clean_links:
							text = re.sub(r'\[.*?\|(.*?)\]','\g<1>',text)
						text = re.sub(r'\<.*?\>',' ',text)
						current_post_comments.append(text)
						# Здесь начинается часть для домашки
						userid = str(comment['id'])
						if userid[0] != '-':
							Succeed = False
							while (not Succeed):
								response = urllib.request.urlopen("https://api.vk.com/method/users.get?user_ids=%s&fields=bdate,city&name_case=Nom&access_token=%s&v=5.69" % (userid, token))
								json_string = response.read().decode('utf-8')
								current_request = json.loads(json_string)
								try:
									current_request['response'][0]
									Succeed = True
								except:
									print('Failed to get request for User, resending')
									Succeed = False
							user = current_request['response'][0]
							if "city" in user:
								user_city_id = user["city"]["id"]
								user_city_name = user["city"]["title"]
								if "bday" in user:
									if len(user["bday"])>=8:
										bday = datetime.datetime.strptime(user["bdate"],"%d.%m.%Y")
										now = datetime.datetime.now()
										user_age = relativedelta(now, bday).years
										cur.execute("INSERT INTO Comments (Comment, CommentLength, Author_id, AuthorAge, AuthorCity, AuthorCity_id) VALUES (?, ?, ?, ?, ?, ?)", [text, CountLength(text), int(userid), user_age, user_city_name, user_city_id])
										conn.commit()
									else:
										cur.execute("INSERT INTO Comments (Comment, CommentLength, Author_id, AuthorCity, AuthorCity_id) VALUES (?, ?, ?, ?, ?)", [text, CountLength(text), int(userid), user_city_name, user_city_id])
										conn.commit()
								else:
									cur.execute("INSERT INTO Comments (Comment, CommentLength, Author_id, AuthorCity, AuthorCity_id) VALUES (?, ?, ?, ?, ?)", [text, CountLength(text), int(userid), user_city_name, user_city_id])
									conn.commit()
							else:
								if "bday" in user:
									if len(user["bday"])>=8:
										bday = datetime.datetime.strptime(user["bdate"],"%d.%m.%Y")
										now = datetime.datetime.now()
										user_age = relativedelta(now, bday).years
										cur.execute("INSERT INTO Comments (Comment, CommentLength, Author_id, AuthorAge) VALUES (?, ?, ?, ?)", [text, CountLength(text), int(userid), user_age])
										conn.commit()
						# Здесь заканчивается часть для домашки
					except:
						print('Exception caught while processing comments')
				Dict[str(item['id'])]['Comments']=current_post_comments
				# Здесь начинается часть для домашки
				cpcl = [CountLength(cmnt) for cmnt in current_post_comments]
				if len(current_post_comments) == 0:
					current_post_mean_comments_length = 0.0
				else:
					current_post_mean_comments_length = float(sum(cpcl)/len(current_post_comments))
				cur.execute("INSERT INTO public%s (id, Post, PostLength, MeanCommentsLength) VALUES (?, ?, ?, ?)" % public_id[1:], [item["id"], Dict[str(item['id'])]['Text'], CountLength(Dict[str(item['id'])]['Text']), current_post_mean_comments_length])
				conn.commit()
				# Здесь заканчивается часть для домашки
		except Exception as e:
			print(str(e)+' happened while processing posts')
	
	keysarr = list(Dict.keys())
	shuffle(keysarr)
	
	i=0
	for key in keysarr:
		i+=1
		filename = key+'.txt'
		with open(filename,'w',encoding='utf-8') as outfile:
			outfile.write(Dict[key]['Text']+'\n')
			if verbose:
				print("Written entity %s" % key)
			if include_comments:
				for comment in Dict[key]['Comments']:
					outfile.write(comment+'\n')
				if verbose:
					print("Written comments for entity %s" % key)
			outfile.write('\n')
		if i == rand_choice:
			break
	
	return public_id

# Здесь начинается часть для домашки
def AccountThisMess(public_id):
	conn = sqlite3.connect('db.sqlite')
	cur = conn.cursor()
	# Dealing with length
	cur.execute("SELECT PostLength FROM public%s" % public_id[1:])
	plens = [Length[0] for Length in cur.fetchall()]
	cur.execute("SELECT MeanCommentsLength FROM public%s" % public_id[1:])
	mclens = [Length[0] for Length in cur.fetchall()]
	plens_s = set(sorted(plens))
	LengthDict = {pl: [] for pl in plens_s}
	for i in range(len(plens)):
		LengthDict[plens[i]].append(mclens[i])
	for key in list(LengthDict.keys()):
		LengthDict[key] = float(sum(LengthDict[key])/len(LengthDict[key]))
	# Same with age
	cur.execute("SELECT AuthorAge FROM Comments")
	ages = [Age[0] for Age in cur.fetchall()]
	cur.execute("SELECT CommentLength FROM Comments")
	clens = [Length[0] for Length in cur.fetchall()]
	ages_s = set(ages)
	AgesDict = {age: [] for age in ages_s}
	for i in range(len(ages)):
		AgesDict[ages[i]].append(clens[i])
	for key in list(AgesDict.keys()):
		AgesDict[key] = float(sum(AgesDict[key])/len(AgesDict[key]))
	# Same with cities
	cur.execute("SELECT AuthorCity FROM Comments")
	cities = [City[0] for City in cur.fetchall()]
	cur.execute("SELECT CommentLength FROM Comments")
	clens = [Length[0] for Length in cur.fetchall()]
	cities_s = set(cities)
	CitiesDict = {city: [] for city in cities_s}
	for i in range(len(cities)):
		CitiesDict[cities[i]].append(clens[i])
	for key in list(CitiesDict.keys()):
		CitiesDict[key] = float(sum(CitiesDict[key])/len(CitiesDict[key]))

	# Plot for post/comment length interrelation
	Length = sorted(list(LengthDict.keys()))
	CommsLens = [length/LengthDict[length] for length in Length if LengthDict[length] != 0]
	Length = [l for l in Length if LengthDict[l] != 0]
	
	objects = set(Length)
	y_pos = np.arange(len(objects))
	 
	plt.plot(y_pos, CommsLens)
	plt.xticks(y_pos, objects)
	plt.ylabel('длина поста/длина комментария')
	plt.title('Отношение длины поста к длине комментария')
	 
	plt.show()

	# Same for age
	Ages = sorted(list(AgesDict.keys()))
	AgesLens = [AgesDict[age] for age in Ages]
	
	objects = set(Ages)
	y_pos = np.arange(len(objects))
	 
	plt.plot(y_pos, AgesLens)
	plt.xticks(y_pos, objects)
	plt.ylabel('Средняя длина комментария')
	plt.title('Возраст')
	 
	plt.show()
		
	# Bars for cities
	Cities = sorted(list(CitiesDict.keys()))
	CitiesLens = [CitiesDict[city] for city in Cities]
	
	objects = set(Cities)
	y_pos = np.arange(len(objects))
	 
	plt.bar(y_pos, CitiesLens, align='center', alpha=0.5)
	plt.xticks(y_pos, objects)
	plt.ylabel('Средняя длина комментария')
	plt.title('Место жительства')
	 
	plt.show()
	
	return 0
# Здесь заканчивается часть для домашки

def make_files():
	# Здесь начинается часть для домашки
	if path.isfile('db.sqlite'): remove('db.sqlite')
	create_connection('db.sqlite')
	# Здесь заканчивается часть для домашки
	
	Wrote = get_posts()
	AccountThisMess(Wrote)
	chdir('..'+sep)
	return Wrote

make_files()
