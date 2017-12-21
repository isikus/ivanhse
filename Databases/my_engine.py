import os

import sqlite3
from sqlite3 import Error

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt


def create_connection(db_file):
	""" create a database connection to a SQLite database """
	try:
		conn = sqlite3.connect(db_file)
		print(sqlite3.version)
	except Error as e:
		print(e)
	finally:
		conn.close()

def getGlossesDict():
	D = {}
	with open('Glossing_rules.txt','r',encoding='windows-1251') as infile:
		lines = infile.readlines()
		for line in lines:
			l = line.split(' — ')
			D[l[0]] = l[1]
	return D

def countPoS():
	conn = sqlite3.connect('db.sqlite')
	cur = conn.cursor()
	cur.execute("SELECT Glosses FROM Words")
	Glosses = [gloss[0] for gloss in cur.fetchall()]
	Dict = getGlossesDict()
	for key in list(Dict.keys()):
		Dict[key] = 0
	for gloss in Glosses:
		if gloss in Dict:
			Dict[gloss] += 1
	Glosses = sorted(list(Dict.keys()))
	Quantity = [Dict[gloss] for gloss in Glosses]
	
	objects = set(Glosses)
	y_pos = np.arange(len(objects))
	 
	plt.bar(y_pos, Quantity, align='center', alpha=0.5)
	plt.xticks(y_pos, objects)
	plt.ylabel('Количество')
	plt.title('Части речи')
	 
	plt.show()
	

if __name__ == '__main__':
	if os.path.isfile('db.sqlite'): os.remove('db.sqlite')
	create_connection('db.sqlite')
		
	Glosses = getGlossesDict()
	
	conn = sqlite3.connect('hittite.db')
	cur = conn.cursor()
	
	cur.execute("SELECT * FROM wordforms")
	rows = cur.fetchall()
	
	Data = []
	for row in rows:
		Data.append(list(row))
	
	conn = sqlite3.connect('db.sqlite')
	cur = conn.cursor()
	cur.execute("CREATE TABLE Words (id INTEGER, Lemma TEXT, Wordform TEXT, Glosses TEXT)")
	cur.execute("CREATE TABLE Glosses (id INTEGER, Gloss TEXT, Description TEXT)")
	cur.execute("CREATE TABLE WordsGlosses (Word_id INTEGER, Gloss_id INTEGER)")
	conn.commit()

	for i in range(len(Data)):
		for entity in Data[i][2].split('.'):
			cur.execute("INSERT INTO Words (id, Lemma, Wordform, Glosses) VALUES (?, ?, ?, ?)", [i+1, Data[i][0], Data[i][1], entity])
	conn.commit()

	contracted = sorted(list(Glosses.keys()))
	for i in range(len(contracted)):
		cur.execute("INSERT INTO Glosses (id, Gloss, Description) VALUES (?, ?, ?)", [i, contracted[i], Glosses[contracted[i]]])
	conn.commit()
	
	cur.execute("SELECT * FROM glosses")
	IDs = {Gloss: id for id, Gloss, nothing in cur.fetchall()}
	for i in range(len(Data)):
		for entity in Data[i][2].split('.'):
			if entity in set(Glosses.keys()):
				cur.execute("INSERT INTO WordsGlosses (Word_id, Gloss_id) VALUES (?, ?)", [i, IDs[entity]])
	conn.commit()
	
	countPoS()