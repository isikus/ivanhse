import urllib.request
from html import unescape
import re
import os

def formatdate(intime):
    outtime = re.sub(' января ','.01.',intime)
    outtime = re.sub(' февраля ','.02.',outtime)
    outtime = re.sub(' марта ','.03.',outtime)
    outtime = re.sub(' апреля ','.04.',outtime)
    outtime = re.sub(' мая ','.05.',outtime)
    outtime = re.sub(' июня ','.06.',outtime)
    outtime = re.sub(' июля ','.07.',outtime)
    outtime = re.sub(' августа ','.08.',outtime)
    outtime = re.sub(' сентября ','.09.',outtime)
    outtime = re.sub(' октября ','.10.',outtime)
    outtime = re.sub(' ноября ','.11.',outtime)
    outtime = re.sub(' декабря ','.12.',outtime)
    return outtime

def clearNl(intext):
    res = intext.replace('\r\n', '')
    res = res.replace('\n', '')
    res = res.replace('\r', '')
    return res

def download_page(pageUrl,eid):
    page = urllib.request.urlopen(pageUrl)
    h = page.read().decode('UTF-8')
    authors = re.findall(r'<div class="news_author" itemprop="author">(.*?)</div>',h,re.DOTALL)
    author = ""
    for name in authors:
        author += name
        author += ', '
    author = author[:-2]
    title = re.search(r'<h1>(.*?)</h1>',h,re.DOTALL).group(1)
    text = unescape(title)
    time = re.search(r'<span class="time">(.*?)</span>',h,re.DOTALL).group(1).split(" ",1)[1]
    date = formatdate(time)
    category = re.search(r'<span class="tags">(.*?)</span>',h,re.DOTALL).group(1)
    category = unescape(category)
    category = re.sub(r'<.*?>','',category,flags=re.DOTALL)
    category = clearNl(category)
    if re.search(r',',category,re.DOTALL) and not re.search(', ',category,re.DOTALL):
        category = re.sub(r',',r', ',category)
    year = date.split(".")[2]
    if date.split(".")[1][0] == "0":
        month = date.split(".")[1][1]
    else:
        month = date.split(".")[1]
    text = re.search(r'<div class="txt js-mediator-article">(.*?)</div>',h,re.DOTALL).group(1)
    text = unescape(text)
    text = re.sub(r'<.*?>',r'',text,flags=re.DOTALL)
    text = re.sub(r'\t',r'',text)

    Words = 0
    for entity in text.split():
        if re.search(r'[a-zA-Zа-яёА-ЯЁ0-9]',entity):
            Words += 1

    if not os.path.isdir(os.path.join('.','plain')):
        os.mkdir(os.path.join('.','plain'))
    if not os.path.isdir(os.path.join('.','mystem-xml')):
        os.mkdir(os.path.join('.','mystem-xml'))
    if not os.path.isdir(os.path.join('.','mystem-plain')):
        os.mkdir(os.path.join('.','mystem-plain'))
    
    if not os.path.isdir(os.path.join('.','plain',year)):
        os.mkdir(os.path.join('.','plain',year))
    if not os.path.isdir(os.path.join('.','plain',year,month)):
        os.mkdir(os.path.join('.','plain',year,month))
    with open(os.path.join('.','plain',year,month,str(eid)+'stub.txt'),"w",encoding="utf-8") as outfile:
        outfile.write(text)

    if not os.path.isdir(os.path.join('.','mystem-xml',year)):
        os.mkdir(os.path.join('.','mystem-xml',year))
    if not os.path.isdir(os.path.join('.','mystem-xml',year,month)):
        os.mkdir(os.path.join('.','mystem-xml',year,month))
    os.system(r"C:\mystem.exe --format xml " + os.path.abspath(os.path.join('.','plain',year,month,str(eid)+'stub.txt')) + ' ' + os.path.abspath(os.path.join('.','mystem-xml',year,month,str(eid)+'.xml')))
    print('Mystem XML written in',os.path.join('.','mystem-xml',year,month,str(eid)+'.xml'))

    if not os.path.isdir(os.path.join('.','mystem-plain',year)):
        os.mkdir(os.path.join('.','mystem-plain',year))
    if not os.path.isdir(os.path.join('.','mystem-plain',year,month)):
        os.mkdir(os.path.join('.','mystem-plain',year,month))
    os.system(r"C:\mystem.exe " + os.path.abspath(os.path.join('.','plain',year,month,str(eid)+'stub.txt')) + ' ' + os.path.abspath(os.path.join('.','mystem-plain',year,month,str(eid)+'.txt')))
    print('Mystem plain written in',os.path.join('.','mystem-plain',year,month,str(eid)+'.txt'))

    os.remove(os.path.join('.','plain',year,month,str(eid)+'stub.txt'))
    with open(os.path.join('.','plain',year,month,str(eid)+'.txt'),"w",encoding="utf-8") as outfile:
        outfile.write('@au '+author+'\n')
        outfile.write('@ti '+title+'\n')
        outfile.write('@da '+date+'\n')
        outfile.write('@topic '+category+'\n')
        outfile.write('@url '+pageUrl+'\n')
        outfile.write('\n')
        outfile.write(text)
        print('URL:',pageUrl,'written in file',os.path.join('.','plain',year,month,str(eid)+'.txt'))
        print(str(Words),'word(s) written')

    Path = os.path.join('.','plain',year,month,str(eid)+'.txt')
    Author = author
    Sex = ""
    Birthday = ""
    Header = title
    Created = date
    Sphere = "публицистика"
    Genre_fi = ""
    Type = ""
    Topic = category
    Chronotop = ""
    Style = "нейтральный"
    Audience_age = "н-возраст"
    Audience_level = "н-уровень"
    Audience_size = "городская"
    Source = pageUrl
    Publication = "МОЁ! Online"
    Publisher = ""
    Publ_year = year
    Medium = "газета"
    Country = "Россия"
    Region = "Воронеж"
    Language = "ru"
    
    return Words, Path, Author, Sex, Birthday, Header, Created, Sphere, Genre_fi, Type, Topic, Chronotop, Style, Audience_age, Audience_level, Audience_size, Source, Publication, Publisher, Publ_year, Medium, Country, Region, Language

totalWords = 0
i = 335078
commonUrl = 'http://www.moe-online.ru/news/view/'
with open("metadata.csv","a",encoding="utf-8") as metadata:
    while i > 334000:
        i-=1
        try:
            print("Creating entity",str(i))
            pageUrl = commonUrl + str(i) + '.html'
            Words, Path, Author, Sex, Birthday, Header, Created, Sphere, Genre_fi, Type, Topic, Chronotop, Style, Audience_age, Audience_level, Audience_size, Source, Publication, Publisher, Publ_year, Medium, Country, Region, Language = download_page(pageUrl,i)
            totalWords += Words
            outstr = '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n'
            metadata.write(outstr % (Path, Author, Sex, Birthday, Header, Created, Sphere, Genre_fi, Type, Topic, Chronotop, Style, Audience_age, Audience_level, Audience_size, Source, Publication, Publisher, Publ_year, Medium, Country, Region, Language))
            print("Metadata written:",outstr % (Path, Author, Sex, Birthday, Header, Created, Sphere, Genre_fi, Type, Topic, Chronotop, Style, Audience_age, Audience_level, Audience_size, Source, Publication, Publisher, Publ_year, Medium, Country, Region, Language))
            print('\n\n'+str(totalWords),"WORDS ALREADY WRITTEN",str(100000-totalWords),"TO GO\nCTRL+C TO INTERRUPT\n\n")
        except Exception as e:
            print('\n\nError at', pageUrl+':',str(e)+'\n\n')
