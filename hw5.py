a={}
total=0
with5=0
with open('intext.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
		total=total+1
        a = line.split(' ')
        if len(a)>4:
			with5=with5+1
print(with5/total*100)
