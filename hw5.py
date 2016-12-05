a={}
total=0
with5=0
with open('intext.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
		total++
        a = line.split(' ', 1)
        if len(a)>4:
			with5++
print(with5/total*100)
