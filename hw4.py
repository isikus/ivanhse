istr=input()
for i in range(len(istr)//2+len(istr)%2):
	print(istr[i:len(istr)-i])
