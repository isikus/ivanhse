import re
import os
from random import shuffle, random, choice

# import sqlite3
import json

from flask import Flask
from flask import render_template
from flask import request

import pyaes
import base64

def encrypt(instr):
	key_128 = b'\xe0\x97\x94|\x0e\xedeP\xcc\x8c\xdc\x95\x16c}X'
	key_hex = "E097947C0EED6550CC8CDC9516637D58"
	
	aes = pyaes.AESModeOfOperationCTR(key_128)
	bytes_raw = bytes(instr, "utf-8")
	bytes_encrypted = aes.encrypt(bytes_raw)
	bytes_encrypted = base64.b32encode(bytes_encrypted)
	encrypted = bytes_encrypted.decode("utf-8")
	return encrypted
	
def decrypt(instr):
	key_128 = b'\xe0\x97\x94|\x0e\xedeP\xcc\x8c\xdc\x95\x16c}X'
	key_hex = "E097947C0EED6550CC8CDC9516637D58"
	
	aes = pyaes.AESModeOfOperationCTR(key_128)
	bytes_encrypted = bytes(instr, "utf-8")
	bytes_encrypted = base64.b32decode(instr)
	bytes_raw = aes.decrypt(bytes_encrypted)
	encrypted = bytes_raw.decode("utf-8")
	return encrypted[0], encrypted[1], encrypted[2:]
	
'''
def SqlInsert(Cursor, TableName, ColumnNames, Values):
	if TableName="":
		return 0
	try:
		if len(ColumnNames) != len(Values):
			return 0
		for i in range(len(Values)):
			req = "INSERT INTO "
			req += TableName
			req += " ("
			req += ColumnNames[i]
			req += ") VALUES (?)"
			Cursor.execute(req, Values[i])
	except:
		try:
			req = "INSERT INTO "
			req += TableName
			req += " ("
			req += ColumnNames
			req += ") VALUES (?)"
			Cursor.execute(req, Values)
		except:
			return 0
	return 1

def GetFromSql(Cursor, TableName, ColumnNames, ConditionStr):
	if TableName="":
		return 0
	try:
		len(ColumnNames)
		try:
			for Column in ColumnNames:
				req = "SELECT "
				req += Column
				req += ", "
			req = req[:-2]
			req += " FROM "
		except:
			req = "SELECT "
			req += ColumnNames
			req += " FROM "
	except:
		req = "SELECT * FROM "
	req += TableName
	try:
		len(ConditionStr)
		req += " WHERE "
		req += ConditionStr
	except:
		pass
	Cursor.execute(req)
	rows = Cursor.fetchall()
	return rows
'''


app = Flask(__name__)

def RenderMe(nameval,Ctx):
	formpiece = """<h3>CTX</h3>
<div class="tcontainer">
<table border="0" cellspacing="3" align="center">
	<tr>
		<td valign="top">
			<input type="radio" name="NAMEVAL" value="0"> Точно нельзя
		</td>
		<td>
			<input type="radio" name="NAMEVAL" value="1"> Скорее нельзя
		</td>
		<td>
			<input type="radio" name="NAMEVAL" value="2"> Ни да ни нет
		</td>
		<td>
			<input type="radio" name="NAMEVAL" value="3"> Скорее можно
		</td>
		<td>
			<input type="radio" name="NAMEVAL" value="4"> Точно можно
		</td>
	</tr>
</table>
</div>"""
	formpiece = re.sub(r"CTX",Ctx,formpiece)
	formpiece = re.sub(r"NAMEVAL",nameval,formpiece)
	return formpiece
	

def generateContexts():
	i = open("testdata.txt","r",encoding="utf-8")
	idiom_M = "за словом в карман не полез"
	idiom_F = "за словом в карман не полезла"
	nkh_M = ["не растерялся", "находчиво заметил", "находчиво отметил"]
	nkh_F = ["не растерялась", "находчиво отметила", "находчиво заметила"]
	kr_M = ["ввернул красное словцо", "красноречиво ответил"]
	kr_F = ["ввернула красное словцо", "красноречиво ответила"]
	ost_M = ["не в бровь, а в глаз заявил", "едко отметил", "едко сказал", "едко ответил", "едко заметил"]
	ost_F = ["не в бровь, а в глаз заявила", "едко отметила", "едко сказала", "едко ответила", "едко заметил"]
	neutr_M = ["ввернул слово", "выпалил", "высказался"]
	neutr_F = ["ввернула слово", "выпалила", "высказалась"]
	neutrconstr = ["убедительно","спокойно","бодро","громко","четко"]
	neutrconstr2 = ["ответил", "сказал", "заявил"]
	contexts = i.readlines()
	Contexts = []
	for context in contexts:
		replstr = ""
		R = random()
		if context[0] == 'I':
			TypeCtx="I"
			if context[1] == 'F':
				ctx = context[2:]
				if R <= 0.35:
					TypeRepl="I"
					replstr = idiom_F
				elif R <= 0.5:
					TypeRepl="S"
					R2 = random()
					if R2 <= 0.333:
						replstr = choice(nkh_F)
					elif R2 <= 0.666:
						replstr = choice(kr_F)
					else:
						replstr = choice(ost_F)
				else:
					TypeRepl="N"
					R2 = random()
					if R2 <= 0.333:
						replstr = choice(neutr_F)
					else:
						replstr = choice(neutrconstr)
						replstr += ' '
						replstr += choice(neutrconstr2)
						replstr += 'а'
				Contexts.append(TypeCtx+TypeRepl+re.sub(r'___.*___',replstr,ctx))
			else:
				ctx = context[1:]
				if R <= 0.35:
					TypeRepl="I"
					replstr = idiom_M
				elif R <= 0.5:
					TypeRepl="S"
					R2 = random()
					if R2 <= 0.333:
						replstr = choice(nkh_M)
					elif R2 <= 0.666:
						replstr = choice(kr_M)
					else:
						replstr = choice(ost_M)
				else:
					TypeRepl="N"
					R2 = random()
					if R2 <= 0.333:
						replstr = choice(neutr_M)
					else:
						replstr = choice(neutrconstr)
						replstr += ' '
						replstr += choice(neutrconstr2)
				Contexts.append(TypeCtx+TypeRepl+re.sub(r'___.*___',replstr,ctx))
		elif context[0] == 'S':
			TypeCtx="S"
			if context[1] == 'F':
				ctx = context[2:]
				if R <= 0.35:
					TypeRepl="I"
					replstr = idiom_F
				elif R <= 0.5:
					TypeRepl="S"
					R2 = random()
					if R2 <= 0.333:
						replstr = choice(nkh_F)
					elif R2 <= 0.666:
						replstr = choice(kr_F)
					else:
						replstr = choice(ost_F)
				else:
					TypeRepl="N"
					R2 = random()
					if R2 <= 0.333:
						replstr = choice(neutr_F)
					else:
						replstr = choice(neutrconstr)
						replstr += ' '
						replstr += choice(neutrconstr2)
						replstr += 'а'
				Contexts.append(TypeCtx+TypeRepl+re.sub(r'___.*___',replstr,ctx))
			else:
				ctx = context[1:]
				if R <= 0.35:
					TypeRepl="I"
					replstr = idiom_M
				elif R <= 0.5:
					TypeRepl="S"
					R2 = random()
					if R2 <= 0.333:
						replstr = choice(nkh_M)
					elif R2 <= 0.666:
						replstr = choice(kr_M)
					else:
						replstr = choice(ost_M)
				else:
					TypeRepl="N"
					R2 = random()
					if R2 <= 0.333:
						replstr = choice(neutr_M)
					else:
						replstr = choice(neutrconstr)
						replstr += ' '
						replstr += choice(neutrconstr2)
				Contexts.append(TypeCtx+TypeRepl+re.sub(r'___.*___',replstr,ctx))
		else:
			TypeCtx="R"
			if context[1] == 'F':
				ctx = context[2:]
				if R <= 0.3:
					TypeRepl="I"
					replstr = idiom_F
				elif R <= 0.45:
					TypeRepl="S"
					R2 = random()
					if R2 <= 0.333:
						replstr = choice(nkh_F)
					elif R2 <= 0.666:
						replstr = choice(kr_F)
					else:
						replstr = choice(ost_F)
				else:
					TypeRepl="N"
					R2 = random()
					if R2 <= 0.333:
						replstr = choice(neutr_F)
					else:
						replstr = choice(neutrconstr)
						replstr += ' '
						replstr += choice(neutrconstr2)
						replstr += 'а'
				Contexts.append(TypeCtx+TypeRepl+re.sub(r'___.*___',replstr,ctx))
			else:
				ctx = context[1:]
				if R <= 0.3:
					TypeRepl="I"
					replstr = idiom_M
				elif R <= 0.45:
					TypeRepl="S"
					R2 = random()
					if R2 <= 0.333:
						replstr = choice(nkh_M)
					elif R2 <= 0.666:
						replstr = choice(kr_M)
					else:
						replstr = choice(ost_M)
				else:
					TypeRepl="N"
					R2 = random()
					if R2 <= 0.333:
						replstr = choice(neutr_M)
					else:
						replstr = choice(neutrconstr)
						replstr += ' '
						replstr += choice(neutrconstr2)
				Contexts.append(TypeCtx+TypeRepl+re.sub(r'___.*___',replstr,ctx))
	shuffle(Contexts)
	return Contexts


# createtest()

def initialiseJSON():
	if not os.path.isfile('data.json'):
		json_view = {}

		for entity in ["sex", "age", "occupation", "birthplace", "residence"]:
			json_view[entity] = []

		for tc in ["I", "S", "R"]:
			for tr in ["I", "S", "N"]:
				colname = tr
				colname += "_in_"
				colname += tc
				colname = re.sub(r"I","idiom",colname)
				colname = re.sub(r"N","neutral",colname)
				colname = re.sub(r"S","swear",colname)
				colname = re.sub(r"R","random",colname)
				json_view[colname] = []
				
		with open('json.json','w',encoding='utf-8') as json_file:
			json.dump(json_view, json_file, ensure_ascii = False, indent = 4)

	return 0

@app.route('/')
def HelloPage():
	initialiseJSON()

	if request.args:
		return mainquestionnary()
   
	return render_template("index.html")

@app.route('/questionnary')
def mainquestionnary():
	'''
	conn = sqlite3.connect('data.sqlite')
	cur = conn.cursor()
	'''

	with open('json.json','r',encoding='utf-8') as f:
		json_view = json.load(f)
	
	metanames = list(request.args.keys())
	answers = []
	for name in metanames:
		answers.append(request.args[name])
		json_view[name].append(request.args[name])
	
	with open('json.json','w',encoding='utf-8') as f:
		json.dump(json_view, f, ensure_ascii = False, indent = 4)
	
	# SqlInsert(cur, "distributed", metanames, answers)
	# SqlInsert(cur, "contexts", metanames, answers)

	Contexts = generateContexts()
	
	bytestrs = []
	output = ""
	
	for Context in Contexts:
		bytestr = encrypt(Context)
		output += RenderMe(bytestr, Context[2:])
		bytestrs.append(bytestr)
	
	namesout = str(bytestrs)
	
	return render_template("questionnary.html", names = namesout, maindata = output)

@app.route('/complete')
def complete():
	'''
	conn = sqlite3.connect('data.sqlite')
	cur = conn.cursor()
	'''

	with open('json.json','r',encoding='utf-8') as f:
		json_view = json.load(f)
	
	bytestrs = sorted(list(request.args.keys()))
	
	TypeCtx = []
	TypeRepl = []
	Contexts = []
	
	for bytestr in bytestrs:
		tc, tr, ctx = decrypt(bytestr)
		TypeCtx.append(tc)
		TypeRepl.append(tr)
		Contexts.append(ctx)
	

	
	answers = []
	for i in range(len(bytestrs)):
		answers.append(request.args[bytestrs[i]])
		json_view[Contexts[i]].append(request.args[bytestrs[i]])
	
	with open('json.json','w',encoding='utf-8') as f:
		json.dump(json_view, f, ensure_ascii = False, indent = 4)
	
	# SqlInsert(cur, "distributed", , answers)
	
	current = 0
	total = 0
	
	TypeCtxs = set(TypeCtx)
	TypeRepls = set(TypeRepl)
	for tc in TypeCtxs:
		for tr in TypeRepls:
			for i in range(len(TypeCtx)):
				if TypeCtx[i] == tc and TypeRepl[i] == tr:
					current += answers[i]
					total += 1
			colname = tr
			colname += "_in_"
			colname += tc
			colname = re.sub(r"I","idiom",colname)
			colname = re.sub(r"N","neutral",colname)
			colname = re.sub(r"S","swear",colname)
			colname = re.sub(r"R","random",colname)
			json_view[colname].append(current/float(total))

	return render_template("complete.html")

@app.route('/json')
def printjson():
	f = open('json.json','r',encoding='utf-8')
	return render_template("json.html", json_data = f.read())
	
if __name__ == '__main__':
	app.run(debug=True)

