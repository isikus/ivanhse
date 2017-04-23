import os

def countfiles(path):
    dic = {}
    for root, dirs, files in os.walk('.'):
        dic[len(files)] = root
    return dic[sorted(list(dic.keys()))[len(list(dic.keys()))-1]]

def main():
    print(countfiles('.'))

main()
