import re

def cleanword(word):
    word=word.lower()
#   print(word)
    falsechars = []
    for i in range(len(word)):
        if re.search("[a-яё\-]",word[i]) == None:
            falsechars.append(word[i])
    for char in falsechars:
        word = word.replace(char,"")
    if word == '-':
        word = ''
    return word

def main():
	with open ('profession.txt' , 'r', encoding='utf-8') as f:
		sentences = re.split(r'([.?!]|(\.\.\.)) ',re.sub(r'[\t\n]',' ',f.read()))
		for sentence in sentences:
			if not sentence:
				continue
			lexemes = [cleanword(word) for word in sentence.split() if cleanword(word)]
			dic = {lexeme: 0 for lexeme in lexemes}
			for lexeme in lexemes:
				dic[lexeme]=dic[lexeme]+1
			outdic = {key: dic[key] for key in sorted(list(dic.keys())) if dic[key] > 1}
			template = '{} {:^10}'
			for wrd in sorted(list(outdic.keys())):
				print(template.format(wrd,outdic[wrd]))

main()
