import random

NEXTGENDER=""
NEXTCASE="nom"
NEEDSVERB=False
ISANIM=False

def sylls(word):
	outs=0
	word=word.lower()
	for i in range(len(word)):
		if word[i]=='а' or word[i]=='е' or word[i]=='ё' or word[i]=='и' or word[i]=='о' or word[i]=='у' or word[i]=='ы' or word[i]=='э' or word[i]=='ю' or word[i]=='я':
			outs = outs + 1
	return outs	

def verb(category,min_syllables,max_syllables):
	global NEXTCASE
	global NEXTGENDER
	if category == "past_m":
		past_m = []
		f = open("v_past_m.txt", 'r', encoding='utf-8')
		for word in f:
			past_m.append(word)
		NEXTGENDER="m"
		pick = random.choice(past_m)[:-1]
		while sylls(pick) < min_syllables or sylls(pick) > max_syllables:
			pick = random.choice(past_m)[:-1]
		return pick
	if category == "past_n":
		past_n = []
		f = open("v_past_n.txt", 'r', encoding='utf-8')
		for word in f:
			past_n.append(word)
		NEXTGENDER="n"
		pick = random.choice(past_n)[:-1]
		while sylls(pick) < min_syllables or sylls(pick) > max_syllables:
			pick = random.choice(past_n)[:-1]
		return pick
	if category == "past_f":
		past_f = []
		f = open("v_past_f.txt", 'r', encoding='utf-8')
		for word in f:
			past_f.append(word)
		NEXTGENDER="f"
		pick = random.choice(past_f)[:-1]
		while sylls(pick) < min_syllables or sylls(pick) > max_syllables:
			pick = random.choice(past_f)[:-1]
		return pick
	else:
		present = []
		f = open("v_praes_tran.txt", 'r', encoding='utf-8')
		for word in f:
			present.append(word)
		pick = random.choice(present)[:-1]
		while sylls(pick) < min_syllables or sylls(pick) > max_syllables:
			pick = random.choice(present)[:-1]
		NEXTCASE="acc"
		return pick

def bigram(gender,min_syllables,max_syllables):
	global NEXTCASE
	casearr=[]
	bigramarr=[]
	if gender == "m":
		f = open("v_abl_m.txt", 'r', encoding='utf-8')
		for word in f:
			bigramarr.append(word)
			casearr.append("abl")
		f = open("v_acc_m.txt", 'r', encoding='utf-8')
		for word in f:
			bigramarr.append(word)
			casearr.append("acc")
		f = open("v_dat_m.txt", 'r', encoding='utf-8')
		for word in f:
			bigramarr.append(word)
			casearr.append("dat")
		f = open("v_gen_m.txt", 'r', encoding='utf-8')
		for word in f:
			bigramarr.append(word)
			casearr.append("gen")
	elif gender == "f":
		f = open("v_abl_f.txt", 'r', encoding='utf-8')
		for word in f:
			bigramarr.append(word)
			casearr.append("abl")
		f = open("v_acc_f.txt", 'r', encoding='utf-8')
		for word in f:
			bigramarr.append(word)
			casearr.append("acc")
		f = open("v_dat_f.txt", 'r', encoding='utf-8')
		for word in f:
			bigramarr.append(word)
			casearr.append("dat")
		f = open("v_gen_f.txt", 'r', encoding='utf-8')
		for word in f:
			bigramarr.append(word)
			casearr.append("gen")		
	else:
		f = open("v_abl_n.txt", 'r', encoding='utf-8')
		for word in f:
			bigramarr.append(word)
			casearr.append("abl")
		f = open("v_acc_n.txt", 'r', encoding='utf-8')
		for word in f:
			bigramarr.append(word)
			casearr.append("acc")
		f = open("v_dat_n.txt", 'r', encoding='utf-8')
		for word in f:
			bigramarr.append(word)
			casearr.append("dat")
		f = open("v_gen_n.txt", 'r', encoding='utf-8')
		for word in f:
			bigramarr.append(word)
			casearr.append("gen")
	pick = random.randint(0,len(bigramarr)-1)
	res = bigramarr[pick][:-1]
	while sylls(res) < min_syllables or sylls(res) > max_syllables:
		pick = random.randint(0,len(bigramarr)-1)
		res = bigramarr[pick][:-1]
	NEXTCASE=casearr[pick]
	return res

def noun(case,gender,min_syllables,max_syllables):
	global NEXTCASE
	global NEXTGENDER
	global ISANIM
	if case == "nom":
		nomnouns = []
		nomgenders = []
		c=0
		f = open("nouns_f_nom.txt", 'r', encoding='utf-8')
		for word in f:
			nomnouns.append(word)
			nomgenders.append("f")
		if gender == "f":
			pick = nomnouns[random.randint(c,len(nomnouns)-1)][:-1]
			while sylls(pick) < min_syllables or sylls(pick) > max_syllables:
				pick = nomnouns[random.randint(c,len(nomnouns)-1)][:-1]
			return pick
		c = len(nomnouns)
		f = open("nouns_m_nom.txt", 'r', encoding='utf-8')
		for word in f:
			nomnouns.append(word)
			nomgenders.append("m")
		if gender == "m":
			pick = nomnouns[random.randint(c,len(nomnouns)-1)][:-1]
			while sylls(pick) < min_syllables or sylls(pick) > max_syllables:
				pick = nomnouns[random.randint(c,len(nomnouns)-1)][:-1]
			return pick
		c = len(nomnouns)		
		f = open("nouns_n_nom.txt", 'r', encoding='utf-8')
		for word in f:
			nomnouns.append(word)
			nomgenders.append("n")
		if gender == "n":
			pick = nomnouns[random.randint(c,len(nomnouns)-1)][:-1]
			while sylls(pick) < min_syllables or sylls(pick) > max_syllables:
				pick = nomnouns[random.randint(c,len(nomnouns)-1)][:-1]
			return pick
		else:
			s = random.randint(c,len(nomnouns)-1)
			pick = nomnouns[s][:-1]
			while sylls(pick) < min_syllables or sylls(pick) > max_syllables:
				s = random.randint(c,len(nomnouns)-1)
				pick = nomnouns[s][:-1]
			NEXTGENDER = nomgenders[s]
			return pick
	if case == "gen":
		gennouns = []
		c=0
		f = open("nouns_f_gen.txt", 'r', encoding='utf-8')
		for word in f:
			gennouns.append(word)
		if gender == "f":
			pick = gennouns[random.randint(c,len(gennouns)-1)][:-1]
			while sylls(pick) < min_syllables or sylls(pick) > max_syllables:
				pick = gennouns[random.randint(c,len(gennouns)-1)][:-1]
			return pick
		c = len(gennouns)
		f = open("nouns_m_gen.txt", 'r', encoding='utf-8')
		for word in f:
			gennouns.append(word)
		if gender == "m":
			pick = gennouns[random.randint(c,len(gennouns)-1)][:-1]
			while sylls(pick) < min_syllables or sylls(pick) > max_syllables:
				pick = gennouns[random.randint(c,len(gennouns)-1)][:-1]
			return pick
		c = len(gennouns)		
		f = open("nouns_n_gen.txt", 'r', encoding='utf-8')
		for word in f:
			gennouns.append(word)
		if gender == "n":
			pick = gennouns[random.randint(c,len(gennouns)-1)][:-1]
			while sylls(pick) < min_syllables or sylls(pick) > max_syllables:
				pick = gennouns[random.randint(c,len(gennouns)-1)][:-1]
			return pick
		else:
			pick = gennouns[random.randint(0,len(gennouns)-1)][:-1]
			while sylls(pick) < min_syllables or sylls(pick) > max_syllables:
				pick = gennouns[random.randint(0,len(gennouns)-1)][:-1]
			return pick	
	if case == "dat":
		datnouns = []
		c=0
		f = open("nouns_f_dat.txt", 'r', encoding='utf-8')
		for word in f:
			datnouns.append(word)
		if gender == "f":
			pick = datnouns[random.randint(c,len(datnouns)-1)][:-1]
			while sylls(pick) < min_syllables or sylls(pick) > max_syllables:
				pick = datnouns[random.randint(c,len(datnouns)-1)][:-1]
			return pick
		c = len(datnouns)
		f = open("nouns_m_dat.txt", 'r', encoding='utf-8')
		for word in f:
			datnouns.append(word)
		if gender == "m":
			pick = datnouns[random.randint(c,len(datnouns)-1)][:-1]
			while sylls(pick) < min_syllables or sylls(pick) > max_syllables:
				pick = datnouns[random.randint(c,len(datnouns)-1)][:-1]
			return pick
		c = len(datnouns)		
		f = open("nouns_n_dat.txt", 'r', encoding='utf-8')
		for word in f:
			datnouns.append(word)
		if gender == "n":
			pick = datnouns[random.randint(c,len(datnouns)-1)][:-1]
			while sylls(pick) < min_syllables or sylls(pick) > max_syllables:
				pick = datnouns[random.randint(c,len(datnouns)-1)][:-1]
			return pick
		else:
			pick = datnouns[random.randint(0,len(datnouns)-1)][:-1]
			while sylls(pick) < min_syllables or sylls(pick) > max_syllables:
				pick = datnouns[random.randint(0,len(datnouns)-1)][:-1]
			return pick	
	if case == "ins":
		insnouns = []
		c=0
		f = open("nouns_f_ins.txt", 'r', encoding='utf-8')
		for word in f:
			insnouns.append(word)
		if gender == "f":
			pick = insnouns[random.randint(c,len(insnouns)-1)][:-1]
			while sylls(pick) < min_syllables or sylls(pick) > max_syllables:
				pick = insnouns[random.randint(c,len(insnouns)-1)][:-1]
			return pick
		c = len(insnouns)
		f = open("nouns_m_ins.txt", 'r', encoding='utf-8')
		for word in f:
			insnouns.append(word)
		if gender == "m":
			pick = insnouns[random.randint(c,len(insnouns)-1)][:-1]
			while sylls(pick) < min_syllables or sylls(pick) > max_syllables:
				pick = insnouns[random.randint(c,len(insnouns)-1)][:-1]
			return pick
		c = len(insnouns)		
		f = open("nouns_n_ins.txt", 'r', encoding='utf-8')
		for word in f:
			insnouns.append(word)
		if gender == "n":
			pick = insnouns[random.randint(c,len(insnouns)-1)][:-1]
			while sylls(pick) < min_syllables or sylls(pick) > max_syllables:
				pick = insnouns[random.randint(c,len(insnouns)-1)][:-1]
			return pick
		else:
			pick = insnouns[random.randint(0,len(insnouns)-1)][:-1]
			while sylls(pick) < min_syllables or sylls(pick) > max_syllables:
				pick = insnouns[random.randint(0,len(insnouns)-1)][:-1]
			return pick
	if case == "abl":
		ablnouns = []
		c=0
		f = open("nouns_f_abl.txt", 'r', encoding='utf-8')
		for word in f:
			ablnouns.append(word)
		if gender == "f":
			pick = ablnouns[random.randint(c,len(ablnouns)-1)][:-1]
			while sylls(pick) < min_syllables or sylls(pick) > max_syllables:
				pick = ablnouns[random.randint(c,len(ablnouns)-1)][:-1]
			return pick
		c = len(ablnouns)
		f = open("nouns_m_abl.txt", 'r', encoding='utf-8')
		for word in f:
			ablnouns.append(word)
		if gender == "m":
			pick = ablnouns[random.randint(c,len(ablnouns)-1)][:-1]
			while sylls(pick) < min_syllables or sylls(pick) > max_syllables:
				pick = ablnouns[random.randint(c,len(ablnouns)-1)][:-1]
			return pick
		c = len(ablnouns)		
		f = open("nouns_n_abl.txt", 'r', encoding='utf-8')
		for word in f:
			ablnouns.append(word)
		if gender == "n":
			pick = ablnouns[random.randint(c,len(ablnouns)-1)][:-1]
			while sylls(pick) < min_syllables or sylls(pick) > max_syllables:
				pick = ablnouns[random.randint(c,len(ablnouns)-1)][:-1]
			return pick
		else:
			pick = ablnouns[random.randint(0,len(ablnouns)-1)][:-1]
			while sylls(pick) < min_syllables or sylls(pick) > max_syllables:
				pick = ablnouns[random.randint(0,len(ablnouns)-1)][:-1]
			return pick
	else:
		accnouns = []
		c=0
		f = open("nouns_f_acc.txt", 'r', encoding='utf-8')
		for word in f:
			accnouns.append(word)
		if gender == "f":
			pick = accnouns[random.randint(c,len(accnouns)-1)][:-1]
			while sylls(pick) < min_syllables or sylls(pick) > max_syllables:
				pick = accnouns[random.randint(c,len(accnouns)-1)][:-1]
			return pick
		c = len(accnouns)
		f = open("nouns_m_acc_anim.txt", 'r', encoding='utf-8')
		for word in f:
			accnouns.append(word)
		if gender == "m" and ISANIM:
			s = random.randint(c,len(accnouns)-1)
			pick = accnouns[s][:-1]
			while sylls(pick) < min_syllables or sylls(pick) > max_syllables:
				s = random.randint(c,len(accnouns)-1)
				pick = accnouns[s][:-1]
			return pick
		c = len(accnouns)	
		f = open("nouns_m_acc_inan.txt", 'r', encoding='utf-8')
		for word in f:
			accnouns.append(word)
		if gender == "m":
			s = random.randint(c,len(accnouns)-1)
			pick = accnouns[s][:-1]
			while sylls(pick) < min_syllables or sylls(pick) > max_syllables:
				s = random.randint(c,len(accnouns)-1)
				pick = accnouns[s][:-1]
			return pick
		c = len(accnouns)		
		f = open("nouns_n_acc.txt", 'r', encoding='utf-8')
		for word in f:
			accnouns.append(word)
		if gender == "n":
			pick = accnouns[random.randint(c,len(accnouns)-1)][:-1]
			while sylls(pick) < min_syllables or sylls(pick) > max_syllables:
				pick = accnouns[random.randint(c,len(accnouns)-1)][:-1]
			return pick
		else:
			pick = accnouns[random.randint(0,len(accnouns)-1)][:-1]
			while sylls(pick) < min_syllables or sylls(pick) > max_syllables:
				pick = accnouns[random.randint(0,len(accnouns)-1)][:-1]
			return pick

def adj(case,min_syllables,max_syllables):
	global NEXTCASE
	global NEXTGENDER
	global ISANIM
	if case == "nom":
		nomarr = []
		nomgender = []
		f = open("adj_f_nom.txt", 'r', encoding='utf-8')
		for word in f:
			nomarr.append(word)
			nomgender.append("f")
		f = open("adj_m_nom.txt", 'r', encoding='utf-8')
		for word in f:
			nomarr.append(word)
			nomgender.append("m")
		f = open("adj_n_nom_acc.txt", 'r', encoding='utf-8')
		for word in f:
			nomarr.append(word)
			nomgender.append("n")
		s = random.randint(0,len(nomarr)-1)
		pick = nomarr[s][:-1]
		while sylls(pick) < min_syllables or sylls(pick) > max_syllables:
			s = random.randint(0,len(nomarr)-1)
			pick = nomarr[s][:-1]
		NEXTGENDER=nomgender[s]
		return pick
	if case == "gen":
		genarr = []
		gengender = []
		f = open("adj_f_gen_dat_ins_abl.txt", 'r', encoding='utf-8')
		for word in f:
			genarr.append(word)
			gengender.append("f")
		f = open("adj_mn_gen.txt", 'r', encoding='utf-8')
		for word in f:
			genarr.append(word)
			gengender.append("m")
		f = open("adj_mn_gen.txt", 'r', encoding='utf-8')
		for word in f:
			genarr.append(word)
			gengender.append("n")
		s = random.randint(0,len(genarr)-1)
		pick = genarr[s][:-1]
		while sylls(pick) < min_syllables or sylls(pick) > max_syllables:
			s = random.randint(0,len(genarr)-1)
			pick = genarr[s][:-1]
		NEXTGENDER=gengender[s]
		return pick
	if case == "dat":
		datarr = []
		datgender = []
		f = open("adj_f_gen_dat_ins_abl.txt", 'r', encoding='utf-8')
		for word in f:
			datarr.append(word)
			datgender.append("f")
		f = open("adj_mn_dat.txt", 'r', encoding='utf-8')
		for word in f:
			datarr.append(word)
			datgender.append("m")
		f = open("adj_mn_dat.txt", 'r', encoding='utf-8')
		for word in f:
			datarr.append(word)
			datgender.append("n")
		s = random.randint(0,len(datarr)-1)
		pick = datarr[s][:-1]
		while sylls(pick) < min_syllables or sylls(pick) > max_syllables:
			s = random.randint(0,len(datarr)-1)
			pick = datarr[s][:-1]
		NEXTGENDER=datgender[s]
		return pick
	if case == "ins":
		insarr = []
		insgender = []
		f = open("adj_f_gen_dat_ins_abl.txt", 'r', encoding='utf-8')
		for word in f:
			insarr.append(word)
			insgender.append("f")
		f = open("adj_mn_ins.txt", 'r', encoding='utf-8')
		for word in f:
			insarr.append(word)
			insgender.append("m")
		f = open("adj_mn_ins.txt", 'r', encoding='utf-8')
		for word in f:
			insarr.append(word)
			insgender.append("n")
		s = random.randint(0,len(insarr)-1)
		pick = insarr[s][:-1]
		while sylls(pick) < min_syllables or sylls(pick) > max_syllables:
			s = random.randint(0,len(insarr)-1)
			pick = insarr[s][:-1]
		NEXTGENDER=insgender[s]
		return pick
	if case == "abl":
		ablarr = []
		ablgender = []
		f = open("adj_f_gen_dat_ins_abl.txt", 'r', encoding='utf-8')
		for word in f:
			ablarr.append(word)
			ablgender.append("f")
		f = open("adj_mn_abl.txt", 'r', encoding='utf-8')
		for word in f:
			ablarr.append(word)
			ablgender.append("m")
		f = open("adj_mn_abl.txt", 'r', encoding='utf-8')
		for word in f:
			ablarr.append(word)
			ablgender.append("n")
		s = random.randint(0,len(ablarr)-1)
		pick = ablarr[s][:-1]
		while sylls(pick) < min_syllables or sylls(pick) > max_syllables:
			s = random.randint(0,len(ablarr)-1)
			pick = ablarr[s][:-1]
		NEXTGENDER=ablgender[s]
		return pick
	else:
		accarr = []
		accgender = []
		f = open("adj_f_acc.txt", 'r', encoding='utf-8')
		for word in f:
			accarr.append(word)
			accgender.append("f")
		if ISANIM:
			f = open("adj_m_acc_anim.txt", 'r', encoding='utf-8')
			for word in f:
				accarr.append(word)
				accgender.append("m")
		else:
			f = open("adj_m_acc_inan.txt", 'r', encoding='utf-8')
			for word in f:
				accarr.append(word)
				accgender.append("m")
		f = open("adj_n_nom_acc.txt", 'r', encoding='utf-8')
		for word in f:
			accarr.append(word)
			accgender.append("n")
		s = random.randint(0,len(accarr)-1)
		pick = accarr[s][:-1]
		while sylls(pick) < min_syllables or sylls(pick) > max_syllables:
			s = random.randint(0,len(accarr)-1)
			pick = accarr[s][:-1]
		NEXTGENDER=accgender[s]
		return pick

def adv():
	advs = []
	f = open("adv.txt", 'r', encoding='utf-8')
	for word in f:
		advs.append(word)
	return random.choice(advs)[:-1]

def punctuation(isend):
	marks = [".", "?", "!", "...", ","]
	r = random.choice(marks)
	while r=="," and isend!="nonend":
		r = random.choice(marks)
	return r

def verbverse7():
	global NEXTCASE
	global NEXTGENDER
	global NEEDSVERB	
	s=""
	sylls_here=0
	opt = random.choice([1,2,3])
	if opt == 1 or opt == 2:
		s=bigram(NEXTGENDER,1,4)
		sylls_here=sylls(s)
		s+=' '
		if sylls_here >= 3:
			s+=noun(NEXTCASE,"indiff",7-sylls_here,7-sylls_here)
		else:
			s+=adj(NEXTCASE,2,3)
			sylls_here=sylls(s)
			s+=' '
			s+=noun(NEXTCASE,NEXTGENDER,7-sylls_here,7-sylls_here)
		s+=punctuation("nonend")
		s=s.capitalize()
		NEEDSVERB=False
	else:
		b="past_"
		b+=NEXTGENDER
		s+=verb(b,1,3)
		sylls_here=sylls(s)
		s=s.capitalize()
		s+=punctuation("end")
		s+=' '
		s+=adj("nom",2,2).capitalize()
		sylls_here=sylls(s)
		s+=' '
		s+=noun("nom",NEXTGENDER,7-sylls_here,7-sylls_here)
	return s

def verbverse5():
	global NEXTGENDER
	global NEEDSVERB
	s=adv()
	sylls_here=sylls(s)
	s+=' '
	b="past_"
	b+=NEXTGENDER
	s+=verb(b,5-sylls_here,5-sylls_here)
	s+=punctuation("nonend")
	s=s.capitalize()
	NEEDSVERB=False
	return s

def verse7a():
	global NEXTGENDER
	sylls_here=0
	v=verb("present_trans",2,3)
	sylls_here=sylls(v)
	v+=' '
	v+=adj("acc",2,5-sylls_here)
	sylls_here=sylls(v)
	v+=' '
	v+=noun("acc",NEXTGENDER,7-sylls_here,7-sylls_here)
	v+=punctuation("nonend")
	v=v.capitalize()
	return v
	
def verse7b():
	global NEXTGENDER
	sylls_here=0
	v=adj("nom",2,3)
	sylls_here=sylls(v)
	v+=' '
	v+=noun("nom",NEXTGENDER,5-sylls_here,5-sylls_here)
	v+=' '
	b="past_"
	b+=NEXTGENDER
	v+=verb(b,2,2)
	v+=punctuation("nonend")
	v=v.capitalize()
	return v

def verse7c():
	global NEXTGENDER
	sylls_here=0
	v=adv()
	sylls_here=sylls(v)
	v+=' '
	verse = random.choice([1,2,3])
	if verse == 1:
		v+=verb("past_m",2,5-sylls_here)
	elif verse == 2:
		v+=verb("past_f",2,5-sylls_here)
	else:
		v+=verb("past_n",2,5-sylls_here)
	sylls_here=sylls(v)
	v+=' '
	v+=noun("nom",NEXTGENDER,7-sylls_here,7-sylls_here)
	v+=punctuation("nonend")
	v=v.capitalize()
	return v

def verse5a():
	global NEXTCASE
	sylls_here=0
	v=verb("present_nontrans",2,3)
	sylls_here=sylls(v)
	v+=' '
	v+=noun(NEXTCASE,"indiff",5-sylls_here,5-sylls_here)
	v+=punctuation("nonend")
	v=v.capitalize()
	return v

def verse5b():
	global NEXTGENDER
	global NEEDSVERB
	sylls_here=0
	v=adj("nom",2,3)
	sylls_here=sylls(v)
	v+=' '
	v+=noun("nom",NEXTGENDER,5-sylls_here,5-sylls_here)
	v=v.capitalize()
	NEEDSVERB=True
	return v
	
def verse5c():
	global NEXTGENDER
	sylls_here=0
	v=noun("nom","indiff",2,3)
	sylls_here=sylls(v)
	v+=' '
	b="past_"
	b+=NEXTGENDER
	v+=verb(b,5-sylls_here,5-sylls_here)
	v=v.capitalize()
	v+=punctuation("nonend")
	return v	
	
def make_verse7():
	global NEEDSVERB
	if NEEDSVERB:
		return verbverse7()
	verse = random.choice([1,2,3])
	if verse == 1:
		return verse7a()
	elif verse == 2:
		return verse7b()
	else:
		return verse7c()

def make_verse5():
	global NEEDSVERB
	if NEEDSVERB:
		return verbverse5()
	verse = random.choice([1,2,3])
	if verse == 1:
		return verse5a()
	elif verse == 2:
		return verse5b()
	else:
		return verse5c()


for n in range(random.randint(1,5)):
	print(make_verse5())
	print(make_verse7())
	print(make_verse5())
	print(make_verse7())
	lastv=make_verse7()
	if lastv[-3:] == "...":
		lastv = lastv[:-3]+punctuation("end")
	else:
		lastv = lastv[:-1]+punctuation("end")
	print(lastv)
	print()
