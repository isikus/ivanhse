arr=[]
for i in range(8):
    inpstr=input()
    arr.append(inpstr)
for i in range(4):
    print(arr[i*2]+arr[i*2+1])
