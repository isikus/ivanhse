import re

def main():
    with open("birds.html",'r',encoding='utf-8') as file:
        f = file.read()
        f = re.sub(r'([^а-яё])птиц((у|ы|а(м?и?|х?)|е)?[^а-яё])',r'\1рыб\2',f)
        f = re.sub(r'([^а-яё])птицей([^а-яё])',r'\1рыбой\2',f)
        f = re.sub(r'([^а-яё])Птиц((у|ы|а(м?и?|х?)|е)?[^а-яё])',r'\1Рыб\2',f)
        f = re.sub(r'([^а-яё])Птицей([^а-яё])',r'\1Рыбой\2',f)
    with open("fishes.html",'w',encoding='utf-8') as outfile:
        outfile.write(f)

main()
